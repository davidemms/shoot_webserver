import threading
import random
import string
import time

from flask import Flask, url_for, render_template, request, send_file, redirect
from flask.helpers import make_response

from . import shoot_wrapper

app = Flask(__name__)

default_newick_str = "()myroot"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/faq')
def faq():
    return render_template("faq.html")


@app.route('/help')
def help():
    return render_template("help.html")


def return_species_tree_page(newick_str, tree_name):    
    return render_template("result.html", 
            newick_str=newick_str,
            query_gene_name=tree_name, 
            gene_webpage_url = "",
            error="")


@app.route('/SpeciesTree_Metazoa')
def SpeciesTree_Metazoa():
    newick_str = "(Dictyostelium_discoideum,(((Saccharomyces_cerevisiae,Phaeosphaeria_nodorum),Schizosaccharomyces_pombe),(Monosiga_brevicollis,(Amphimedon_queenslandica,(Mnemiopsis_leidyi,(((Nematostella_vectensis,Thelohanellus_kitauei),Trichoplax_adhaerens),(((Octopus_bimaculoides,(Schistosoma_mansoni,Helobdella_robusta)),((Trichinella_spiralis,Caenorhabditis_elegans),(Ixodes_scapularis,(Daphnia_magna,((Bombyx_mori,((Glossina_morsitans,Drosophila_melanogaster),Anopheles_gambiae)),Apis_mellifera))))),(Strongylocentrotus_purpuratus,(Branchiostoma_lanceolatum,(Ciona_intestinalis,(Petromyzon_marinus,((Callorhinchus_milii,(Latimeria_chalumnae,((Leptobrachium_leishanense,Xenopus_tropicalis),((Ornithorhynchus_anatinus,((Phascolarctos_cinereus,Monodelphis_domestica),((Bos_taurus,Canis_familiaris),((Callithrix_jacchus,(Pan_troglodytes,Homo_sapiens)),(Mus_musculus,Rattus_norvegicus))))),(Anolis_carolinensis,(Chrysemys_picta,(Crocodylus_porosus,(Gallus_gallus,(Bubo_bubo,Corvus_moneduloides))))))))),(Lepisosteus_oculatus,(Danio_rerio,(Oncorhynchus_mykiss,(Gadus_morhua,(Tetraodon_nigroviridis,(Astatotilapia_calliptera,(Oryzias_latipes,Poecilia_formosa)))))))))))))))))));"
    return return_species_tree_page(newick_str, "Metazoa")


@app.route('/SpeciesTree_Fungi')
def SpeciesTree_Fungi():
    newick_str = "(Dictyostelium_discoideum:1.1455384,((Monosiga_brevicollis:1.23131,(Caenorhabditis_elegans:1.26457,(Homo_sapiens:0.61205,Drosophila_melanogaster:0.86926)N9:0.12555)N6:0.18301)N3:0.16406,(((Encephalitozoon_intestinalis:1.05763,Enterocytozoon_bieneusi:1.40798)N4:1.29381,(((Mortierella_elongata:0.63058,Rhizopus_delemar:0.69301)N10:0.11964,(Batrachochytrium_salamandrivorans:0.76586,Spizellomyces_punctatus:0.51048)N11:0.32327)N7:0.08617,((Puccinia_graminis:0.96814,(Ustilago_maydis:0.86728,(Cryptococcus_neoformans:0.83352,(Rhizoctonia_solani:0.52938,(Agaricus_bisporus:0.33543,Amanita_muscaria:0.32567)N23:0.257)N19:0.18508)N16:0.12767)N14:0.06884)N12:0.21454,(Schizosaccharomyces_pombe:1.13217,((Yarrowia_lipolytica:0.795,(Saccharomyces_cerevisiae:0.83669,Candida_albicans:0.74887)N20:0.30498)N17:0.28172,(((Aspergillus_nidulans:0.1965,Aspergillus_fumigatus:0.16541)N24:0.37669,(Phaeosphaeria_nodorum:0.48559,Zymoseptoria_tritici:0.5072)N25:0.11515)N21:0.05616,(((Colletotrichum_graminicola:0.25641,Fusarium_oxysporum:0.30789)N28:0.08691,(Magnaporthe_oryzae:0.35769,Neurospora_crassa:0.33785)N29:0.06007)N26:0.18556,(Blumeria_graminis:0.46514,(Sclerotinia_sclerotiorum:0.06331,Botrytis_cinerea:0.05458)N30:0.22498)N27:0.11692)N22:0.14265)N18:0.43341)N15:0.10152)N13:0.21594)N8:0.1357)N5:0.12158)N2:0.06347)N0:0.06347)N1:0.0602915);"
    return return_species_tree_page(newick_str, "Fungi")

@app.route('/SpeciesTree_Plants')
def SpeciesTree_Plants():
    newick_str = "((Cyanidioschyzon_merolae:1.13166,(Chondrus_crispus:0.76391,Galdieria_sulphuraria:0.83788)0.774:0.1204)1:0.27888,(((Chlamydomonas_reinhardtii:0.1964,Volvox_carteri:0.25442)1:0.69377,(Micromonas_spRCC299:0.45615,Ostreococcus_lucimarinus:0.87149)1:0.38254)0.759:0.10776,(Chara_braunii:0.74837,((Physcomitrella_patens:0.63651,(Marchantia_polymorpha:0.54869,Anthoceros_punctatus:0.56867)0.741:0.05515)1:0.06785,((Selaginella_moellendorffii:0.68271,Azolla_filiculoides:0.64147)0.959:0.11009,((Gingko_biloba:0.25115,(Picea_glauca:0.06054,Pinus_sylvestris:0.07333)1:0.24025)1:0.28736,(Amborella_trichopoda:0.6917,((Spirodela_polyrhiza:0.64394,(Musa_acuminata:0.38714,((Zea_mays:0.16648,Setaria_italica:0.11481)1:0.10895,(Oryza_sativa:0.22837,(Triticum_aestivum:0.08658,Hordeum_vulgare:0.06695)1:0.20214)0.998:0.04117)1:0.52664)1:0.10355)1:0.14101,(Aquilegia_coerulea:0.55414,(Solanum_lycopersicum:0.66539,((Glycine_max:0.62318,Eucalyptus_grandis:0.44257)0.977:0.05657,(Prunus_persica:0.4681,((Brassica_oleracea:0.16547,Arabidopsis_thaliana:0.13697)1:0.59799,(Gossypium_raimondii:0.38689,Manihot_esculenta:0.43943)0.929:0.04351)0.95:0.03347)0.996:0.05112)1:0.05709)1:0.09442)1:0.11986)1:0.15081)1:0.25661)1:0.19026)0.907:0.06323)1:0.22889)1:0.27407)1:0.27888);"
    return return_species_tree_page(newick_str, "Plants")


@app.route('/SpeciesTree_UniProt')
def SpeciesTree_UniProt():
    # newick_str_of_version = "((((Chloroflexus_aurantiacus:0.77879,(Halobacterium_salinarum:1.59696,((Methanosarcina_acetivorans:1.0006,Methanocaldococcus_jannaschii:0.81148)0.962:0.25482,((Saccharolobus_solfataricus:1.18515,Chlamydia_trachomatis:1.09328)0.759:0.25158,((Korarchaeum_cryptofilum:1.26797,Nitrosopumilus_maritimus:1.04693)0.006:0.05579,(Thermococcus_kodakarensis:0.91576,Fusobacterium_nucleatum:0.87744)0.957:0.20104)0.965:0.14528)0.253:0.07402)0.711:0.12047)0.095:0.12211)0.757:0.12615,((Rhodopirellula_baltica:1.4722,(((Bacillus_subtilis:0.73351,Deinococcus_radiodurans:0.90237)0.977:0.17711,(Mycobacterium_tuberculosis:0.48322,Streptomyces_coelicolor:0.54017)1:0.55721)0.693:0.0933,(Gloeobacter_violaceus:0.85274,((Dictyoglomus_turgidum:0.64224,Thermotoga_maritima:1.03194)1:0.21175,(Geobacter_sulfurreducens:0.63454,(Trichomonas_vaginalis:0.97091,(Thermodesulfovibrio_yellowstonii:0.61597,Aquifex_aeolicus:0.64596)0.399:0.04192)0.418:0.0681)0.44:0.09952)0.965:0.09116)0.754:0.06696)1:0.19629)0.107:0.07528,(Bradyrhizobium_diazoefficiens:0.90864,(Pseudomonas_aeruginosa:0.384,(Escherichia_coli:0.42314,Neisseria_meningitidis:0.4582)0.959:0.15159)1:0.31028)1:0.25022)0.634:0.06058)1:0.19849,((Leptospira_interrogans:1.11647,(Paramecium_tetraurelia:1.00893,Bacteroides_thetaiotaomicron:0.67402)0.826:0.30061)0.654:0.12121,(Plasmodium_falciparum:1.58035,(Helicobacter_pylori:1.17316,Mycoplasma_genitalium:1.3399)0.674:0.08186)0.188:0.10537)0.858:0.12272)1:0.09778,((Giardia_intestinalis:2.12871,Leishmania_major:1.70325)0.982:0.15898,(Dictyostelium_discoideum:1.08804,(((Phytophthora_ramorum:0.97142,Thalassiosira_pseudonana:1.28959)1:0.2212,(Chlamydomonas_reinhardtii:0.98251,((Physcomitrella_patens:0.46744,(Arabidopsis_thaliana:0.35363,(Zea_mays:0.12675,Oryza_sativa:0.10357)1:0.26933)1:0.28678)1:0.27819,Synechocystis_sp.:0.63652)0.604:0.04883)1:0.2849)1:0.09295,((Batrachochytrium_dendrobatidis:0.98083,((Schizosaccharomyces_pombe:1.06449,((Yarrowia_lipolytica:0.78568,(Candida_albicans:0.71093,Saccharomyces_cerevisiae:0.81321)1:0.29298)1:0.25881,((Neurospora_crassa:0.46911,Sclerotinia_sclerotiorum:0.36917)1:0.14822,(Neosartorya_fumigata:0.4688,Phaeosphaeria_nodorum:0.51857)1:0.06789)1:0.4017)1:0.09426)1:0.19563,(Ustilago_maydis:0.87008,(Puccinia_graminis:0.89814,Cryptococcus_neoformans:0.85211)0.975:0.08824)1:0.24235)1:0.14765)1:0.19861,(Monosiga_brevicollis:1.20056,(Caenorhabditis_elegans:1.40127,((Helobdella_robusta:0.92034,(Ciona_intestinalis:0.84675,(Nematostella_vectensis:0.65504,(Branchiostoma_floridae:0.50427,((Lepisosteus_oculatus:0.16298,(Oryzias_latipes:0.22253,Danio_rerio:0.18573)1:0.07637)1:0.0934,(Xenopus_tropicalis:0.2366,(Gallus_gallus:0.17953,(Monodelphis_domestica:0.12251,((Mus_musculus:0.02577,Rattus_norvegicus:0.02868)1:0.06748,((Homo_sapiens:0.00265,(Pan_troglodytes:0.00413,Gorilla_gorilla:0.00713)1:0.00423)1:0.04156,(Canis_lupus:0.06464,Bos_taurus:0.05791)1:0.01409)0.916:0.01158)1:0.08435)1:0.0777)1:0.06287)1:0.06666)1:0.30315)1:0.07502)0.996:0.04897)0.967:0.05876)0.818:0.04298,(Ixodes_scapularis:0.7449,((Drosophila_melanogaster:0.52551,Anopheles_gambiae:0.49858)1:0.22537,Tribolium_castaneum:0.57495)1:0.24785)1:0.08758)1:0.14552)1:0.10765)1:0.13898)1:0.07579)0.96:0.07015)1:0.12484)1:0.09778)"
    newick_str_partially_resolved = "(((((Korarchaeum_cryptofilum,Nitrosopumilus_maritimus),Sulfolobus_solfataricus),((Trichomonas_vaginalis,Giardia_intestinalis),(Leishmania_major,((((Plasmodium_falciparum,Paramecium_tetraurelia),(Phytophthora_ramorum,Thalassiosira_pseudonana)),(Chlamydomonas_reinhardtii,(Physcomitrella_patens,(Arabidopsis_thaliana,(Oryza_sativa,Zea_mays))))),(Dictyostelium_discoideum,((Batrachochytrium_dendrobatidis,((Puccinia_graminis,(Ustilago_maydis,Cryptococcus_neoformans)),(Schizosaccharomyces_pombe,(((Candida_albicans,Saccharomyces_cerevisiae),Yarrowia_lipolytica),((Neurospora_crassa,Sclerotinia_sclerotiorum),(Neosartorya_fumigata,Phaeosphaeria_nodorum)))))),(Monosiga_brevicollis,(Nematostella_vectensis,(Branchiostoma_floridae,((Helobdella_robusta,(Caenorhabditis_elegans,(Ixodes_scapularis,(Tribolium_castaneum,(Drosophila_melanogaster,Anopheles_gambiae))))),(Ciona_intestinalis,(((Danio_rerio,Oryzias_latipes),Lepisosteus_oculatus),(Xenopus_tropicalis,(Gallus_gallus,(Monodelphis_domestica,(((Homo_sapiens,(Pan_troglodytes,Gorilla_gorilla)),(Rattus_norvegicus,Mus_musculus)),(Bos_taurus,Canis_lupus))))))))))))))))),((Methanosarcina_acetivorans,Halobacterium_salinarum),Thermococcus_kodakarensis,Methanocaldococcus_jannaschii)),(((Escherichia_coli,Pseudomonas_aeruginosa),Neisseria_meningitidis,Bradyrhizobium_diazoefficiens,Helicobacter_pylori,Geobacter_sulfurreducens),(Synechocystis_sp.,Mycobacterium_tuberculosis,Streptomyces_coelicolor),Bacillus_subtilis,Bacteroides_thetaiotaomicron,Deinococcus_radiodurans,Leptospira_interrogans,Thermotoga_maritima,Chlamydia_trachomatis,Gloeobacter_violaceus,Thermodesulfovibrio_yellowstonii,Mycoplasma_genitalium,Fusobacterium_nucleatum,Rhodopirellula_baltica,Chloroflexus_aurantiacus,Aquifex_aeolicus,Dictyoglomus_turgidum))"
    return return_species_tree_page(newick_str_partially_resolved, "UniProt Reference Proteomes 2020 Partially Resolved Species Tree")
   
   
@app.route('/SpeciesTree_Prokaryotes')
def SpeciesTree_Prokaryotes():
    newick_str_partially_resolved = "((((((Pseudaminobacter_manganicus:1,Phyllobacterium_YR620:1)Phyllobacteriaceae:1,(Agrobacterium_fabrum:1,Rhizobium_leguminosarum:1,Neorhizobium_NCHU2750:1)Rhizobium_Agrobacterium_group:1,(Bradyrhizobium_diazoefficiens:1,Bradyrhizobium_LMTRsp3:1)Bradyrhizobium:1,Methylocella_silvestris:1,Aureimonas_Leaf454:1,Chelatococcus_CO-6:1,Bosea_RAC05:1,Methylobacterium_durans:1)Hyphomicrobiales:1,(((Novosphingobium_malaysiense:1,Novosphingobium_MD-1:1)Novosphingobium:1,(Sphingomonas_turrisvirgatae:1,(Sphingomonas_IBVSS2:1,Sphingomonas_TF3:1)unclassified_Sphingomonas:1)Sphingomonas:1,Sphingobium_japonicum:1)Sphingomonadaceae:1,Erythrobacter_HI00D59:1)Sphingomonadales:1,((Komagataeibacter_medellinensis:1,Roseicella_frigidaeris:1)Acetobacteraceae:1,Roseospirillum_parvum:1)Rhodospirillales:1,((Mameliella_alba:1,Confluentimicrobium_lipolyticum:1,Loktanella_IMCC34160:1)Roseobacteraceae:1,(Gemmobacter_caeni:1,Paracoccus_sulfuroxidans:1)Rhodobacteraceae:1,Rhodobacterales_bacterium:1)Rhodobacterales:1,Rickettsiales_bacterium:1,Brevundimonas_S30B:1)Alphaproteobacteria:1,(((Klebsiella_pneumoniae:1,Shigella_flexneri:1,Salmonella_typhimurium:1,Escherichia_coli:1,Candidatus_Tachikawaea:1)Enterobacteriaceae:1,(Yersinia_pestis:1,Serratia_marcescens:1)Yersiniaceae:1,Proteus_mirabilis:1,Sodalis_praecaptivus:1,Brenneria_goodwinii:1)Enterobacterales:1,((Acinetobacter_calcoaceticus:1,Acinetobacter_indicus:1)Acinetobacter:1,(Pseudomonas_guangdongensis:1,Pseudomonas_aeruginosa:1,Pseudomonas_HLS-6:1)Pseudomonas:1)Pseudomonadales:1,((Marinobacter_similis:1,Marisediminitalea_aggregata:1)Alteromonadaceae:1,Colwellia_psychrerythraea:1,Pseudoalteromonas_piscicida:1)Alteromonadales:1,((Stenotrophomonas_panacihumi:1,Pseudoxanthomonas_composti:1)Xanthomonadaceae:1,Dyella_M7H15-1:1)Xanthomonadales:1,(Thiogranum_longum:1,Wenzhouxiangella_W260:1)Chromatiales:1,(Haemophilus_influenzae:1,Haemophilus_parasuis:1)Pasteurellaceae:1,(Vibrio_cholerae:1,Vibrio_hepatarius:1)Vibrio:1,(Legionella_pneumophila:1,Legionella_TUM19329:1)Legionella:1,Cardiobacterium_hominis:1,Microbulbifer_ZGT114:1,Piscirickettsia_litoralis:1,Halomonas_sp1513:1)Gammaproteobacteria:1,(((Sorangium_cellulosum:1,Melittangium_boletus:1)Myxococcales:1,(Geobacter_sulfurreducens:1,Geothermobacter_EPR-M:1)Geobacteraceae:1,Desulfovibrio_vulgaris:1,Desulfonema_ishimotonii:1)Deltaproteobacteria:1,((Campylobacter_jejuni:1,Campylobacter_12-5580:1)Campylobacter:1,(Helicobacter_pylori:1,Helicobacter_hepaticus:1)Helicobacter:1,Sulfurimonas_GYSZ1:1)Campylobacterales:1)delta_epsilon_subdivisions:1,((Neisseria_meningitidis:1,Chromobacterium_LK11:1)Neisseriales:1,((Acidovorax_JS42:1,Pelomonas_puraquae:1,Rhodoferax_IMCC26218:1)Comamonadaceae:1,Paraburkholderia_lacunae:1,Aquabacterium_KMB7:1,Massilia_lurida:1,Parapusillimonas_SGNA-6:1)Burkholderiales:1,Thauera_linaloolentis:1,Candidatus_Accumulibacter:1,Nitrosospira_Nsp11:1)Betaproteobacteria:1,Acidithiobacillus_ferrooxidans:1)Proteobacteria:1,((((((Mycolicibacterium_paratuberculosis:1,Mycobacterium_tuberculosis:1)Mycobacterium:1,Mycolicibacterium_fortuitum:1)Mycobacteriaceae:1,Gordonia_polyisoprenivorans:1,(Corynebacterium_imitans:1,Corynebacterium_LMM-1652:1,Corynebacterium_vitaeruminis:1)Corynebacterium:1,Rhodococcus_MTM3W5:1)Corynebacteriales:1,((Aeromicrobium_Root472D3:1,Micropruina_glycogenica:1,Nocardioides_silvaticus:1)Nocardioidaceae:1,Cutibacterium_acnes:1)Propionibacteriales:1,((Microterricola_viridarii:1,Microbacterium_4-13:1,Frondihabitans_PhB188:1,Leucobacter_HDW9A:1)Microbacteriaceae:1,(Arthrobacter_livingstonensis:1,Arthrobacter_Leaf69:1)Arthrobacter:1,Flavimobilis_soli:1,Georgenia_soli:1,Tetrasphaera_F2B08:1)Micrococcales:1,((Microbispora_rosea:1,Nonomuraea_pusilla:1)Streptosporangiaceae:1,Marinitenerispora_sediminis:1,Actinomadura_LD22:1)Streptosporangiales:1,(Streptomyces_curacoi:1,(Streptomyces_SLBN-118:1,Streptomyces_SID8455:1)unclassified_Streptomyces:1,Streptomyces_coelicolor:1)Streptomyces:1,(Scardovia_wiggsiae:1,Bifidobacterium_LMGsp-31471:1)Bifidobacteriaceae:1,Micromonospora_maris:1,Actinobacteria_bacterium:1,Frankia_EI5c:1,Blastococcus_DSMsp-46838:1,Actinomyces_ruminicola:1,(Amycolatopsis_albispora:1,Saccharothrix_australiensis:1,Pseudonocardia_broussonetiae:1)Pseudonocardiaceae:1)Actinomycetia:1,(((Collinsella_massiliensis:1,Coriobacteriaceae_bacterium:1)Coriobacteriaceae:1,Olsenella_F0356:1)Coriobacteriales:1,Eggerthella_CAG209:1)Coriobacteriia:1)Actinobacteria:1,(((((Streptococcus_pneumoniae:1,Streptococcus_sanguinis:1)Streptococcus:1,Lactococcus_lactis:1)Streptococcaceae:1,((Lactobacillus_xujianguonis:1,Lactobacillus_acidophilus:1)Lactobacillus:1,Lactobacillus_coryniformis:1,Paucilactobacillus_wasatchensis:1,Weissella_cibaria:1)Lactobacillaceae:1,(Enterococcus_rivorum:1,Enterococcus_faecalis:1)Enterococcus:1,Globicatella_HMSC072A10:1)Lactobacillales:1,((((Bacillus_FJAT-21945:1,Bacillus_UMB0899:1)unclassified_Bacillus_|in__Bacteria|:1,Bacillus_subtilis:1)Bacillus:1,Geobacillus_WCH70:1,Virgibacillus_massiliensis:1,Lysinibacillus_F5:1,Alkalihalobacillus_krulwichiae:1)Bacillaceae:1,((Paenibacillus_rigui:1,Paenibacillus_D14:1)Paenibacillus:1,Brevibacillus_WF146:1)Paenibacillaceae:1,Listeria_monocytogenes:1,(Staphylococcus_aureus:1,Staphylococcus_haemolyticus:1)Staphylococcus:1)Bacillales:1)Bacilli:1,((Dialister_succinatiphilus:1,Megasphaera_An286:1)Veillonellaceae:1,Methylomusa_anaerophila:1)Negativicutes:1,((Clostridioides_difficile:1,Romboutsia_maritimum:1)Peptostreptococcaceae:1,(((Subdoligranulum_CAG314:1,Bacillus_CAG988:1,Firmicutes_bacterium:1,Alistipes_CAG268:1,Prevotella_copri:1)environmental_samples:1,Subdoligranulum_4-3-54A2FAA:1)Subdoligranulum:1,Hungateiclostridium_thermocellum:1,Ruminococcus_albus:1)Oscillospiraceae:1,(Desulfosporosinus_meridiei:1,Pelotomaculum_thermopropionicum:1)Peptococcaceae:1,(Butyrivibrio_proteoclasticus:1,Roseburia_sp499:1,Lachnoclostridium_An76:1,Mobilisporobacter_senegalensis:1)Lachnospiraceae:1,(Gemmiger_formicilis:1,Lawsonibacter_asaccharolyticus:1)Eubacteriales_incertae_sedis:1,((Clostridium_MSTE9:1,Clostridium_chh4-2:1,Clostridium_JN-9:1)unclassified_Clostridium:1,Clostridium_perfringens:1,Clostridium_saccharoperbutylacetonicum:1)Clostridium:1,Caloranaerobacter_azorensis:1)Eubacteriales:1,Absiella_dolichum:1)Firmicutes:1,(Chloroflexus_aurantiacus:1,Dictyobacter_kobayashii:1)Chloroflexi:1,((Synechocystis_Kazusa:1,Synechococcus_CC9311:1)Synechococcales:1,Gloeomargarita_lithophora:1,Gloeobacter_violaceus:1,Rippkaea_orientalis:1,Nostoc_T09:1)Cyanobacteria:1,(((Mycoplasma_equirhinis:1,Mycoplasma_genitalium:1,Mycoplasma_ES2806-GEN:1)Mycoplasma:1,Mycoplasma_canis:1)Mycoplasmataceae:1,Spiroplasma_culicicola:1)Mollicutes:1,(Deinococcus_radiodurans:1,Deinococcus_deserti:1)Deinococcus:1)Terrabacteria_group:1,(Chlamydia_trachomatis:1,((Rhodopirellula_baltica:1,Novipirellula_galeiformis:1)Pirellulaceae:1,Pseudobythopirellula_maris:1)Pirellulales:1,Opitutus_GAS368:1)PVC_group:1,(Nitrospira_japonica:1,Thermodesulfovibrio_yellowstonii:1)Nitrospirae:1,(Thiotrophic_endosymbiont:1,Methanotrophic_endosymbiont:1)unclassified_Bacteria:1,((((Porphyromonas_gingivalis:1,(Bacteroides_thetaiotaomicron:1,Bacteroides_finegoldii:1)Bacteroides:1)Bacteroidales:1,Marinilabilia_salmonicolor:1)Bacteroidia:1,((Dyadobacter_fermentans:1,Spirosoma_oryzae:1)Cytophagaceae:1,Cecembia_lonarensis:1,Hymenobacter_KIGAM108:1)Cytophagales:1,((Salegentibacter_mishustinae:1,Tenacibaculum_holothuriorum:1,(Flavobacterium_FPG59:1,Flavobacterium_CC-CTC003:1)unclassified_Flavobacterium:1,Polaribacter_ALD11:1,Ulvibacter_MAR-2010-11:1,Lacinutrix_CAUsp-1491:1)Flavobacteriaceae:1,Chryseobacterium_taihuense:1)Flavobacteriales:1,(Mucilaginibacter_gossypii:1,Sphingobacterium_lactis:1,Pedobacter_RP-3-15:1)Sphingobacteriaceae:1,(Chitinophaga_barathri:1,Dinghuibacter_silviterrae:1)Chitinophagaceae:1)Bacteroidetes:1,Chlorobium_phaeobacteroides:1)Bacteroidetes_Chlorobi_group:1,((Borrelia_hermsii:1,Treponema_denticola:1)Spirochaetales:1,Leptospira_interrogans:1)Spirochaetia:1,Aquifex_aeolicus:1,(Fusobacterium_nucleatum:1,Fusobacterium_mortiferum:1)Fusobacterium:1,Dictyoglomus_turgidum:1,Thermotoga_maritima:1,TM7_phylum:1,Edaphobacter_12200R-103:1)Bacteria:1,(((((Halobacterium_salinarum:1,Haloarcula_marismortui:1)Halobacteriales:1,Haloterrigena_limicola:1,Halorubrum_halodurans:1)Halobacteria:1,(Methanosarcina_acetivorans:1,Methanosphaerula_palustris:1)Methanomicrobia:1)Stenosarchaea_group:1,(Methanocaldococcus_jannaschii:1,Methanobrevibacter_cuticularis:1)Methanomada_group:1,Thermococcus_kodakarensis:1,Candidate_MSBL1-archaeon:1)Euryarchaeota:1,(Nitrosopumilus_maritimus:1,Korarchaeum_cryptofilum:1,Saccharolobus_solfataricus:1)TACK_group:1)Archaea:1)"
    return return_species_tree_page(newick_str_partially_resolved, "Bacteria & Archaea")
 
 
@app.route('/result', methods=['POST', 'GET'])
def calculating():
    # if method == 'POST':
    error = None
    form = request.form
    submitted_seq_data = form["seq_data"]
    i_db = form["i_database"]
    success_db = False
    success_seq = False
    if len(i_db) <= 2:
        try:
            i_db = int(i_db)
            db_name = shoot_wrapper.get_database(i_db)
            db_url = shoot_wrapper.get_web_url(i_db)
            i_sensitivity = int(form["i_sensitivity"])
            i_dmnd_profiles = int(form["i_dmnd_profiles"])
            i_mafft_options = int(form["i_mafft_options"])
            success_db = True
        except:
            pass
    if success_db:
        success_seq, seq_name, seq, err_string = shoot_wrapper.validate_data(submitted_seq_data)
 
    def run_shoot(server_id, submission_id, seq_name, seq, db_name, 
                    i_sensitivity, i_dmnd_profiles, i_mafft_options):
        shoot_wrapper.run_shoot_remote(
                                    server_id, 
                                    submission_id,
                                    seq_name, 
                                    seq, 
                                    db_name,
                                    i_sensitivity,
                                    i_dmnd_profiles,
                                    i_mafft_options,
                                    )
    
    if success_db and success_seq:
        server_id, _, _, _, _, _ = shoot_wrapper.server.random_config()
        submission_id = ''.join(random.choice(string.ascii_letters) for i in range(16))
        submission_id = str(server_id) + submission_id
        results_url = url_for("result", result_id="%s" % submission_id, _external=True)
        resp = make_response(render_template("waiting.html", results_url=results_url))
        atr_samesite = 'Strict'
        resp.set_cookie('subid', submission_id, samesite=atr_samesite)
        resp.set_cookie('name', seq_name, samesite=atr_samesite)
        resp.set_cookie('idb', str(i_db), samesite=atr_samesite)
        resp.set_cookie('db', db_name, samesite=atr_samesite)
        
        form = request.form
        thread = threading.Thread(target=run_shoot, args=(server_id, submission_id, seq_name, seq, db_name, 
                                                    i_sensitivity, i_dmnd_profiles, i_mafft_options))
        thread.start()
    else:
        newick_str = "()myroot"
        err_string = "ERROR: Submitted sequence was invalid"
        resp = make_response(render_template("result.html", 
                                        newick_str=newick_str, 
                                        query_gene_name="", 
                                        gene_webpage_url="",
                                        error=err_string))
    
    return resp


@app.route('/result/<result_id>', methods=['GET', ])
def result(result_id):
    submission_id = result_id
    seq_name = request.cookies.get('name')
    i_db = int(request.cookies.get('idb'))
    db_url = shoot_wrapper.get_web_url(i_db)
    db_name = shoot_wrapper.get_database(i_db)
    results_url = url_for("result", result_id=submission_id, _external=True)
    for _ in range(10):
        status = shoot_wrapper.is_complete(submission_id)
        if status:
            break
        time.sleep(1)
    if status is False:
        atr_samesite = 'Strict'
        resp = make_response(render_template("waiting.html", results_url=results_url))
        resp.set_cookie('subid', submission_id, samesite=atr_samesite)
    elif status == True:
        ret_val = shoot_wrapper.get_result(submission_id)
        success_shoot = False if ret_val is None else True
        if success_shoot:
            newick_str, err_string, submission_id, iog_str = ret_val
        else:
            newick_str = "()myroot"
            err_string = "ERROR: Submitted sequence was invalid"
        renamed_seq = "SHOOT_" + seq_name
        if renamed_seq in newick_str:
            seq_name = renamed_seq
        
        resp = make_response(render_template("result.html", 
                                        newick_str=newick_str, 
                                        query_gene_name=seq_name, 
                                        gene_webpage_url=db_url,
                                        error=err_string,
                                        results_url=results_url))
        atr_samesite = 'Strict'
        resp.set_cookie('iog', iog_str, samesite=atr_samesite)
        resp.set_cookie('db', db_name, samesite=atr_samesite)
        resp.set_cookie('subid', submission_id, samesite=atr_samesite)
        resp.set_cookie('name', seq_name, samesite=atr_samesite)
        return resp
    #else:
    #    # failure
    #    newick_str = "()myroot"
    #    err_string = "Unknown failure"
    #    resp = make_response(render_template("result.html", 
    #                                    newick_str="();", 
    #                                    query_gene_name="Error", 
    #                                    gene_webpage_url="",
    #                                    error=err_string))
    return resp
        

# @app.route('/result2')
# def result_test():
#     newick_str="(((Blumeria_graminis_BLGH_03519:0.671414,Botrytis_cinerea_Bcin01g09730:0.12327)87:0.115042,(((Colletotrichum_graminicola_GLRG_03987:0.105424,Fusarium_oxysporum_FOXG_00607:0.225705)92:0.0766329,Magnaporthe_oryzae_MGG_04821:0.227089)78:0.0499628,Neurospora_crassa_NCU02739:0.229127)94:0.155455)82:0.0796659,(Zymoseptoria_tritici_Mycgr3G88038:1.03544,(Phaeosphaeria_nodorum_SNOG_12227:0.917734,(Aspergillus_fumigatus_CDV58_08741:0.0782832,Aspergillus_nidulans_ANIA_02113:0.180388)100:0.5926)76:0.191863)82:0.0796659);"
#     seq_name = "a"
#     err_string = ""
#     iog_str = "-1"
#     db_url = ""
#     resp = make_response(render_template("result.html", 
#                                 newick_str=newick_str, 
#                                 query_gene_name=seq_name, 
#                                     gene_webpage_url=db_url,
#                                 error=err_string))
#     atr_samesite = 'Strict'
#     resp.set_cookie('iog', iog_str, samesite=atr_samesite)
#     resp.set_cookie('db', "Results_Mar16", samesite=atr_samesite)
#     resp.set_cookie('subid', "a"*16, samesite=atr_samesite)
#     resp.set_cookie('QUERY_GENE', seq_name, samesite=atr_samesite)
#     return resp


@app.route('/download_fasta', methods=['GET', ])
def download_sequences():
    try:
        err_string = "Data is no longer available, please resubmit your search"
        fn = None
        download_name = None

        iog = request.cookies.get('iog')
        db = request.cookies.get('db')
        subid = request.cookies.get('subid')
        gene_name = request.cookies.get('name')
        n_level = 5   # sensible default
        if request.method == 'GET':
            try:
                n_level_str = request.args.get('tl')
                if n_level_str is not None:
                    n_level = int(n_level_str)
                    if n_level < 0:
                        n_level = None
            except (KeyError, ValueError):
                pass
        if db not in shoot_wrapper.available_databases:
            err_string = "Unrecognised SHOOT database"
        elif not shoot_wrapper.valid_iog_format(iog):
            err_string = "Unrecognised tree"
        elif not shoot_wrapper.valid_subid_format(subid):
            err_string = "Data is no longer available, please resubmit your search"
        elif not shoot_wrapper.valid_gene_name(gene_name):
            err_string = "Invalid gene name"
        else:
            fn = shoot_wrapper.create_fasta_file(db, iog, subid, gene_name, n_level)
            download_name = "shoot_tree_%s_sequences.txt" % gene_name
        if fn is None:
            resp = make_response(render_template("result.html", 
                            newick_str=default_newick_str, 
                            query_gene_name="", 
                            error=err_string))
            return resp
        else:
            return send_file(fn, as_attachment=True, attachment_filename=download_name)
    except Exception as e:
        return str(e)

