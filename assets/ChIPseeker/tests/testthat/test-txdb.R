library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library(TxDb.Hsapiens.UCSC.hg38.knownGene)
library(ChIPseeker)
library(yulab.utils)

context("TXDB")

test_that("Update txdb", {
    hg19_txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
    ChIPseeker:::.ChIPseekerEnv(hg19_txdb)
    expect_equal(ChIPseeker:::get_env_genome(), "hg19")

    hg38_txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene
    ChIPseeker:::.ChIPseekerEnv(hg38_txdb)
    expect_equal(ChIPseeker:::get_env_genome(), "hg38")
})


test_that("txdb", {
    txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
    ChIPseeker:::.ChIPseekerEnv(txdb)
    expect_equal(ChIPseeker:::IDType(txdb), "Entrez Gene ID")

    if (packageVersion("TxDb.Hsapiens.UCSC.hg19.knownGene") > "3.22") {
        expect_equal(
            ChIPseeker:::TXID2EG("70455"),
            "ENST00000487630.1_3/ENST00000487630.1_3"
        )
        expect_equal(
            ChIPseeker:::TXID2EG("70455", geneIdOnly = TRUE),
            "ENST00000487630.1_3"
        )
    } else {
        expect_equal(ChIPseeker:::TXID2EG("70455"), "uc002qsd.4/1")
        expect_equal(ChIPseeker:::TXID2EG("70455", geneIdOnly = TRUE), "1")
    }
})
