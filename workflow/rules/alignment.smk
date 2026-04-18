# Rule: BWA-MEM alignment

rule bwa_mem:
    """
    Align reads to reference genome using BWA-MEM
    
    Critical: Adds read group information (required by GATK!)
    """
    input:
        r1="data/raw/{sample}_R1.fastq.gz",
        r2="data/raw/{sample}_R2.fastq.gz",
        ref=config["reference"]["genome"],
        # Ensure indices exist
        idx=expand("{ref}.{ext}", 
                   ref=config["reference"]["genome"],
                   ext=["bwt", "pac", "ann", "amb", "sa"])
    output:
        temp("{aln}/{{sample}}_aligned.sam".format(
            aln=config["output"]["alignment"]
        ))
    params:
        rg=lambda wildcards: config["params"]["bwa"]["read_group"].format(
            sample=wildcards.sample
        )
    threads: config["params"]["bwa"]["threads"]
    log:
        "logs/bwa/{sample}.log"
    benchmark:
        "benchmarks/bwa/{sample}.txt"
    shell:
        """
        bwa mem \
            -t {threads} \
            -R '{params.rg}' \
            {input.ref} \
            {input.r1} {input.r2} \
            > {output} \
            2> {log}
        """


# Rule: Sort SAM to BAM

rule sam_to_bam:
    """
    Convert SAM to sorted BAM
    """
    input:
        "{aln}/{{sample}}_aligned.sam".format(
            aln=config["output"]["alignment"]
        )
    output:
        temp("{aln}/{{sample}}_sorted.bam".format(
            aln=config["output"]["alignment"]
        ))
    threads: config["params"]["samtools"]["threads"]
    log:
        "logs/samtools/sort_{sample}.log"
    shell:
        """
        samtools sort \
            -@ {threads} \
            -o {output} \
            {input} \
            2> {log}
        """


# Rule: Index Sorted BAM (before markdup)
rule index_sorted_bam:
    """
    Create BAM index for sorted BAMs only
    (markdup and final BAMs create their own indices)
    """
    input:
        "{aln}/{{sample}}_sorted.bam".format(
            aln=config["output"]["alignment"]
        )
    output:
        "{aln}/{{sample}}_sorted.bam.bai".format(
            aln=config["output"]["alignment"]
        )
    log:
        "logs/samtools/index_{sample}_sorted.log"
    shell:
        """
        samtools index {input} 2> {log}
        """
