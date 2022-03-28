
#!/home/omarjee/anaconda3/bin/python



import math
import sys
import os
import subprocess
import argparse

# Definie le dossier principale qui va contenir tout les dossiers créer
doss = os.getcwd()

# arg de notre script
def parse_argument():
    parser = argparse.ArgumentParser(description="Pipeline de fastq  à BAM")
    parser.add_argument("-t", dest="threads", help="Number of threads to use\
    for BAM name sorting", nargs=1)
    parser.add_argument("-s", dest="fasta", help="Fichier génome de référence\
    ", nargs=1)
    parser.add_argument("-f", dest="fastq", help="Fichier fastq à utiliser si\
    vous mettez que le dossier alors tous les fastq seront utiliser \
    ", nargs="+")
    parser.add_argument("-e", dest="end", help="Savoir si c'est single end\
    ou pair end", nargs=1)
    parser.add_argument("-g", dest="gtf", help="Fichier gtf", nargs=1)
    parser.add_argument("-i", dest="index", help="génome indexé", nargs="?",default="index")
    return parser.parse_args()


# Fasta en index
def index(fasta):
    commande = f"STAR --runMode genomeGenerate --genomeDir {indexa} \
     --genomeFastaFiles {fasta[0]}  --sjdbGTFfile {gtf[0]} --runThreadN \
     {threads[0]}"
    print(commande)
    subprocess.call(commande,shell=True)

# detecte l index optionnelle
def check_index(indexa):
    if os.path.exists(indexa):
        print("Index trouvé")
    else:
        sys.exit("L'index fournit ne fonctionne pas")

# Detecte si notre génome de reférence fasta existe
def check_fasta(fasta):
    if os.path.exists(fasta[0]):
        print("Génome de référence trouvé")
    else:
        sys.exit("Le fichier fasta est absent")


# Detecte si nos fichier fastq existe en single ou en double
def check_fastq(fastq, end):
    if end[0] == "single":
        if os.path.exists("fastq/"+fastq[0]):
            print("Le fichier fastq " + fastq[0] + " a été trouvé")
        else:
            sys.exit("Le fichier fastq est absent")
    if end[0] == "pair":
        if os.path.exists("fastq/"+fastq[0]) and os.path.exists("fastq/"+fastq[1]):
            print("Les fichiers fastq " + os.path.basename(fastq[0]) + " et "
            + os.path.basename(fastq[1]) + " ont été trouvés")
        else:
            sys.exit("Les fichiers fastq sont absents ou le dossier fastq n'existe pas")

# Detecte le fichier gtf
def check_gtf(gtf):
    if os.path.exists(gtf[0]):
        print("Le fichier gtf a été trouvé")
    else:
        sys.exit("Le fichier gtf est absent")

# Verification des pass1 avant de les transformer en pass2
def check_pass1(data):
    if data ==[]:
        sys.exit("Erreur: Le dossier pass1 est vide. Vérifiez qu'il contient "
        +"bien des fichiers .sortedByCoord.out.bam")
    else:
        print("pass1 trouvé")

# Verification des pass2 avant de les transformer en bai
def check_pass2(data):
    if data ==[]:
        sys.exit("Erreur : Le dossier pass2 est vide. Vérifiez qu'il contient "
        +"bien des fichiers _pass1_SJ.out.tab")
    else:
        print("pass2 trouvé")

# nomenclature
def prefix(ffastq, enda):
    if enda == "single":
        pre = os.path.splitext(os.path.basename(ffastq[0]))[0]
        pre = pre.split("_")[0]
    if enda == "pair":
        pre1 = os.path.splitext(os.path.basename(ffastq[0]))[0]
        pre2 = os.path.splitext(os.path.basename(ffastq[1]))[0]
        pre = os.path.commonprefix(pre1.split()+ pre2.split())
        pre = pre.split("_")[0]
    if enda == "":
        pre = ffastq.split("_")
    return pre

def recup_fastq():
    data = [file for file in os.listdir(fastq[0]) if file.endswith(".fastq")]
    return data

def recup_pass1():
    data = [file for file in os.listdir("pass1") if file.endswith(".tab")]
    return data

def recup_pass2():
    data = [file for file in os.listdir("pass2") if file.endswith(".sortedByCoord.out.bam")]
    return data

def recup_bai():
    data =  [file for file in os.listdir("pass2") if file.endswith(".sortedByCoord.out.bam.bai")]
    return data

# pour le dossier des pass1
def dossier1():
    for dossier in os.listdir():
        if dossier == "pass1":
            print("Dossier pass1 existe déja")
            return 1
# Création du dossier qui va contenir tous les pass1
    print("Création d'un dossier pass1")
    creationdossier = f"mkdir pass1"
    subprocess.call(creationdossier, shell=True)



# pour les dossiers des pass2
def dossier2():
    for dossier in os.listdir():
        if dossier == "pass2":
            print("Dossier pass2 existe déja")
            return 1
# Création du dossier qui va contenir tous les pass2
    print("Création d'un dossier pass2")
    creationdossier = f"mkdir pass2"
    subprocess.call(creationdossier, shell=True)


# Pour obtenir les pass1 si single ou pair
def commandepass1(fastq, end, pre):
    if end[0] == "single":
        commande = f"STAR --runThreadN {threads[0]} --outSAMtype None --genomeDir {indexa} --readFilesIn fastq/{fastq[0]} --sjdbGTFfile {gtf[0]} --outFileNamePrefix pass1/{pre}pass1_"
    if end[0] == "pair":
        commande = f"STAR --runThreadN {threads[0]} --outSAMtype None --genomeDir {indexa} --readFilesIn fastq/{fastq[0]} fastq/{fastq[1]} --sjdbGTFfile {gtf[0]}  --outFileNamePrefix pass1/{pre}pass1_"
    return commande


# Execution du pass1_ (detection de fastq et pre)
def exepass1():
    dossier1()
    limite = dico["pass1"]
    file = sorted(recup_fastq())
    if os.path.isdir("fastq"):
        for i in range(0, len(file), 2):
            fastq = file[i].split()+file[i+1].split()
            check_fastq(fastq, end)
            pre = prefix(fastq, end[0])
            if pre in limite:
                commande = commandepass1(fastq, end, pre)
                print(commande)
                subprocess.call(commande,shell=True)
    else:
        check_fastq(fastq, end)
        dossier1()
        pre = prefix(fastq, end)
        commande = commandepass1(fastq, end, pre)
        print(commande)
        subprocess.call(commande,shell=True)


# Pour obtenir les pass2 si single ou pair
def commandepass2(fastq, end, pre):
    if end[0] == "single":
        commande = f"STAR --runThreadN 12 --genomeDir {indexa} --readFilesIn {fastq[0]} --sjdbGTFfile gtf[0]--outFileNamePrefix pass2/{pre}_pass2_ --sjdbFileChrStartEnd  *_pass1_SJ.out.tab --outSAMtype BAM SortedByCoordinate --outMultimapperOrder Random --outSAMmultNmax 1 --outFilterMultimapNmax 30 --outFilterMismatchNmax 1"
    if end[0] == "pair":
        commande = f"STAR --runThreadN 12 --genomeDir {indexa} --readFilesIn fastq/{fastq[0]} fastq/{fastq[1]} --sjdbGTFfile {gtf[0]} --outFileNamePrefix pass2/{pre}_pass2_ --sjdbFileChrStartEnd  pass1/*_pass1_SJ.out.tab --outSAMtype BAM SortedByCoordinate --outMultimapperOrder Random --outSAMmultNmax 1 --outFilterMultimapNmax 30 --outFilterMismatchNmax 1 --limitSjdbInsertNsj 1246601"
    return commande


# Commande d execution du/des pass2 (peut faire dossier ou 1 fichiers)
def exepass2():
    dossier2()
    limite = dico["pass2"]
    file = sorted(recup_fastq())
    check_pass1(os.listdir("pass1"))
    if os.path.isdir("fastq"):
        for i in range(0, len(file), 2):
            fastq = file[i].split()+file[i+1].split()
            check_fastq(fastq, end)
            pre = prefix(fastq, end[0])
            if pre in limite:
                commande = commandepass2(fastq, end, pre)
                print(commande)
                subprocess.call(commande,shell=True)
    else:
        check_fastq(fastq, end)
        dossier2()
        pre = prefix(fastq, end)
        commande = commandepass2(fastq, end, pre)
        print(commande)
        subprocess.call(commande,shell=True)


# transformation en bai
def bai():
    data = recup_pass2()
    check_pass2(data)
    limite = dico["bai"]
    os.chdir("pass2")
    for fichier in enumerate(data):
        pre = prefix(fichier[1],"")[0]
        if pre in limite:
            commande = f"samtools index  -@ 12 {fichier[1]}"
            print(commande)
            subprocess.call(commande, shell=True)

def list_fastq():
    fichier = recup_fastq()
    lfas = []
    for i in range(0, len(fichier), 1):
        ffastq = fichier[i].split("_")[0]
        lfas.append(ffastq)
    return lfas

def list_pass1():
    data = recup_pass1()
    lpass = []
    for i in data:
        lpass.append(i.split("_")[0])
    return lpass

def list_pass2():
    data = recup_pass2()
    lpass = []
    for i in data:
        lpass.append(i.split("_")[0])
    return lpass

def list_bai():
    data = recup_bai()
    lpass = []
    for i in data:
        lpass.append(i.split("_")[0])
    return lpass

def check():
    dico ={"fastq":set(list_fastq()),"pass1":set(list_pass1()),"pass2":set(list_pass2()),"bai":list_bai()}
    dico["pass1"] = [elem for elem in dico["fastq"] if elem  not in dico["pass1"]]
    dico["pass2"] = [elem for elem in dico["fastq"] if elem not in dico["pass2"]]
    dico["bai"] = [elem for elem in dico["fastq"] if elem not in dico["bai"]]
    return dico


def main():
    # verification des arg
    check_gtf(gtf)
    check_fasta(fasta)
    if indexa == "index":
        index(fasta)
        print("Index créer")
    check_index(indexa)
    # Lance la commande pour les pass1
    exepass1()
    # Lance la commande pour les pass2
    exepass2()
    # Lance la commande pour les bainars 1 or 0
    bai()

# extraction des arg
result_args = parse_argument()
threads = result_args.threads
fasta = result_args.fasta
fastq = result_args.fastq
gtf = result_args.gtf
end = result_args.end
indexa = result_args.index
    # garde la liste des fastq
dico = check()
main()
