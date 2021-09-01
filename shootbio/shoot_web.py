from flask import Flask, url_for, render_template, request, send_file
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
    
@app.route('/result', methods=['POST', ])
def result():
    error = None
    newick_str = default_newick_str
    seq_name = ""
    db_url = ""
    if request.method == 'POST':
        submitted_data = request.form["seq_data"]
        i_db = request.form["i_database"]
        success_db = False
        db_name = "none"
        if len(i_db) <= 2:
            try:
                i_db = int(i_db)
                success_db = True
                db_name = shoot_wrapper.get_database(i_db)
                db_url = shoot_wrapper.get_web_url(i_db)
            except:
                pass
        if success_db:
            success_seq, seq_name, seq, err_string = shoot_wrapper.validate_data(submitted_data)
        if success_db and success_seq:
            ret_val = shoot_wrapper.run_shoot_remote(seq_name, seq, db_name)
            success_shoot = False if ret_val is None else True
        if success_db and success_seq and success_shoot:
            newick_str, err_string, submission_id, iog_str = ret_val
        else:
            newick_str = "()myroot"
            err_string = "ERROR: Submitted sequence was invalid"
            submission_id = "0"*16
            iog_str = "-1"
    resp = make_response(render_template("result.html", 
                                    newick_str=newick_str, 
                                    query_gene_name=seq_name, 
                                    gene_webpage_url=db_url,
                                    error=err_string))
    atr_samesite = 'Strict'
    resp.set_cookie('iog', iog_str, samesite=atr_samesite)
    resp.set_cookie('db', db_name, samesite=atr_samesite)
    resp.set_cookie('subid', submission_id, samesite=atr_samesite)
    resp.set_cookie('name', seq_name, samesite=atr_samesite)
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

