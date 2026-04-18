"""
Somatic Variant Calling Rules
Mutect2 tumor-normal paired calling
"""


# Rule: Mutect2 Somatic Calling

rule mutect2:
    """
    Call somatic variants using GATK Mutect2
    
    Key: Compares tumor vs normal to find cancer-specific mutations
    """
    input:
        tumor="{aln}/{tumor}_final.bam".format(
            aln=config["output"]["alignment"],
            tumor=TUMOR
        ),
        tumor_bai="{aln}/{tumor}_final.bam.bai".format(
            aln=config["output"]["alignment"],
            tumor=TUMOR
        ),
        normal="{aln}/{normal}_final.bam".format(
            aln=config["output"]["alignment"],
            normal=NORMAL
        ),
        normal_bai="{aln}/{normal}_final.bam.bai".format(
            aln=config["output"]["alignment"],
            normal=NORMAL
        ),
        ref=config["reference"]["genome"]
    output:
        vcf="{variants}/somatic_raw.vcf.gz".format(
            variants=config["output"]["variants"]
        ),
        stats="{variants}/somatic_raw.vcf.gz.stats".format(
            variants=config["output"]["variants"]
        )
    params:
        tumor_name=TUMOR,
        normal_name=NORMAL,
        java_opts=config["params"]["mutect2"]["java_opts"]
    threads: config["params"]["mutect2"]["threads"]
    log:
        "logs/gatk/mutect2.log"
    benchmark:
        "benchmarks/gatk/mutect2.txt"
    shell:
        """
        gatk --java-options '{params.java_opts}' Mutect2 \
            -R {input.ref} \
            -I {input.tumor} -tumor {params.tumor_name} \
            -I {input.normal} -normal {params.normal_name} \
            -O {output.vcf} \
            --native-pair-hmm-threads {threads} \
            2> {log}
        """

# Rule: Filter Mutect Calls

rule filter_mutect:
    """
    Apply filters to raw Mutect2 calls
    Removes false positives
    """
    input:
        vcf="{variants}/somatic_raw.vcf.gz".format(
            variants=config["output"]["variants"]
        ),
        ref=config["reference"]["genome"]
    output:
        vcf="{variants}/somatic_filtered.vcf.gz".format(
            variants=config["output"]["variants"]
        )
    log:
        "logs/gatk/filter_mutect.log"
    shell:
        """
        gatk FilterMutectCalls \
            -R {input.ref} \
            -V {input.vcf} \
            -O {output.vcf} \
            2> {log}
        """


# Rule: Select PASS Variants

rule select_pass:
    """
    Keep only variants that PASS all filters
    """
    input:
        "{variants}/somatic_filtered.vcf.gz".format(
            variants=config["output"]["variants"]
        )
    output:
        "{variants}/somatic_pass.vcf.gz".format(
            variants=config["output"]["variants"]
        )
    log:
        "logs/bcftools/select_pass.log"
    shell:
        """
        bcftools view \
            -f PASS \
            {input} \
            -Oz -o {output} \
            2> {log}
        
        tabix -p vcf {output}
        """
