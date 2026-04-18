"""
Preprocessing Rules
GATK MarkDuplicates (BQSR skipped for test data)
"""

# ==========================================
# Rule: Mark Duplicates
# ==========================================
rule mark_duplicates:
    """
    Mark PCR/optical duplicates using GATK
    Then create BAM index with samtools
    """
    input:
        bam="{aln}/{{sample}}_sorted.bam".format(
            aln=config["output"]["alignment"]
        ),
        bai="{aln}/{{sample}}_sorted.bam.bai".format(
            aln=config["output"]["alignment"]
        )
    output:
        bam="{aln}/{{sample}}_markdup.bam".format(
            aln=config["output"]["alignment"]
        ),
        bai="{aln}/{{sample}}_markdup.bam.bai".format(
            aln=config["output"]["alignment"]
        ),
        metrics="{qc}/picard/{{sample}}_markdup_metrics.txt".format(
            qc=config["output"]["qc"]
        )
    params:
        java_opts=config["params"]["markdup"]["java_opts"]
    log:
        "logs/gatk/markdup_{sample}.log"
    benchmark:
        "benchmarks/gatk/markdup_{sample}.txt"
    shell:
        """
        # Run GATK MarkDuplicates
        gatk --java-options '{params.java_opts}' MarkDuplicates \
            -I {input.bam} \
            -O {output.bam} \
            -M {output.metrics} \
            2> {log}
        
        # Create index with samtools (more reliable than GATK's CREATE_INDEX)
        samtools index {output.bam}
        """

# ==========================================
# Rule: Prepare Final BAM (Skip BQSR for test data)
# ==========================================
rule prepare_final_bam:
    """
    Prepare final analysis-ready BAM
    
    For test data: Skip BQSR (insufficient known sites)
    For production: Enable BQSR with full dbSNP
    """
    input:
        bam="{aln}/{{sample}}_markdup.bam".format(
            aln=config["output"]["alignment"]
        ),
        bai="{aln}/{{sample}}_markdup.bam.bai".format(
            aln=config["output"]["alignment"]
        )
    output:
        bam="{aln}/{{sample}}_final.bam".format(
            aln=config["output"]["alignment"]
        ),
        bai="{aln}/{{sample}}_final.bam.bai".format(
            aln=config["output"]["alignment"]
        )
    log:
        "logs/preprocessing/prepare_final_{sample}.log"
    shell:
        """
        echo "Creating final BAM (BQSR skipped for test data)" > {log}
        echo "Copying from: {input.bam}" >> {log}
        echo "Copying to: {output.bam}" >> {log}
        
        cp {input.bam} {output.bam}
        cp {input.bai} {output.bai}
        
        echo "Final BAM created successfully" >> {log}
        """


