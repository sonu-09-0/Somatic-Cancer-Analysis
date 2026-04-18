"""
Quality Control Rules
FastQC and MultiQC for all samples
"""


# Rule: FastQC on raw reads

rule fastqc:
    """
    Run FastQC on raw FASTQ files
    
    Input: Raw FASTQ (R1 or R2)
    Output: FastQC HTML and ZIP reports
    """
    input:
        "data/raw/{sample}_{read}.fastq.gz"
    output:
        html="{qc}/fastqc/{{sample}}_{{read}}_fastqc.html".format(
            qc=config["output"]["qc"]
        ),
        zip="{qc}/fastqc/{{sample}}_{{read}}_fastqc.zip".format(
            qc=config["output"]["qc"]
        )
    params:
        outdir="{qc}/fastqc".format(qc=config["output"]["qc"])
    threads: config["params"]["fastqc"]["threads"]
    log:
        "logs/fastqc/{sample}_{read}.log"
    benchmark:
        "benchmarks/fastqc/{sample}_{read}.txt"
    shell:
        """
        mkdir -p {params.outdir}
        fastqc {input} \
            --outdir {params.outdir} \
            --threads {threads} \
            2> {log}
        """


# Rule: MultiQC aggregate report

rule multiqc:
    """
    Aggregate all QC reports with MultiQC
    
    Input: All FastQC reports
    Output: Single HTML report
    """
    input:
        expand("{qc}/fastqc/{sample}_{read}_fastqc.zip",
               qc=config["output"]["qc"],
               sample=SAMPLES,
               read=["R1", "R2"])
    output:
        "{qc}/multiqc_report.html".format(qc=config["output"]["qc"])
    params:
        outdir=config["output"]["qc"]
    log:
        "logs/multiqc/multiqc.log"
    shell:
        """
        multiqc {params.outdir} \
            --outdir {params.outdir} \
            --force \
            2> {log}
        """
