BINS = {

    ## RUN II BINNING ##

    'mass4l': '|105|160|',
    'mass4l_zzfloating': '|105|160|',
    'Nj': '|0|1|2|3|4|20|',
    #'pT4l': '|0|10|20|30|45|60|80|120|200|3000|',
    #'pT4l': '|0|10000|',
    #'pT4l': '|0|15|30|45|80|120|200|350|10000|', #HGG
    'pT4l_kL': '|0|45|80|120|200|1300|',

    'costhetaZ1': '|-1.0|-0.75|-0.50|-0.25|0.0|0.25|0.50|0.75|1.0|',
    'costhetaZ2': '|-1.0|-0.75|-0.50|-0.25|0.0|0.25|0.50|0.75|1.0|',
    'phi': '|-3.14159265359|-2.35619449019|-1.57079632679|-0.785398163397|0.0|0.785398163397|1.57079632679|2.35619449019|3.14159265359|',
    'phi1': '|-3.14159265359|-2.35619449019|-1.57079632679|-0.785398163397|0.0|0.785398163397|1.57079632679|2.35619449019|3.14159265359|',
    'costhetastar': '|-1.0|-0.75|-0.50|-0.25|0.0|0.25|0.50|0.75|1.0|',

    'dphijj': '|-100|-3.14159265359|-1.5707963267948966|0|1.5707963267948966|3.14159265359|',

    ## RUN III BINNING 09 02 2026 ##

    "pT4l": "|0|10|16|22|28|36|46|60|80|106|146|10000|",
    "rapidity4l": "|0|0.12|0.24|0.36|0.5|0.6|0.75|0.9|1.1|1.3|10000|",
    "massZ1": "|40|65|75|85|92|120|",
    "massZ2": "|12|22|26|28|32|34|40|50|65|",
    "pTj1": "|-100|30|55|95|200|10000|",
    "mHj": "|-100|0|210|275|355|460|645|10000|",
    "pTHj": "|-100.0|0|12|28|40|85|10000|",
    "pTj2": "|-100|30|45|62|10000|",
    "mjj": "|-100|0|92|224|10000|",
    "absdetajj": "|-100|0|1.1|2.9|4.4|10|",
    "pTHjj": "|-100.0|0.0|25|75|10000|",
    "TCjmax": "|-100.0|0.0|4|8|15|20|35|10000|",
    "TBjmax": "|-100|0|4|8|16|25|45|10000|",

    "rapidity4l vs pT4l": "|0|0.2| vs |0|50| / |0.2|0.4| vs |0|50| / |0.4|0.65| vs |0|50| / |0.65|0.9| vs |0|50| / |0.9|1.2| vs |0|50| / |1.2|2.5| vs |0|50| / |0|0.5| vs |50|105| / |0.5|1.15| vs |50|105| / |1.15|2.5| vs |50|105| / |0|0.45| vs |105|10000| / |0.45|1| vs |105|10000| / |1|2.5| vs |105|10000|",
    "massZ1 vs massZ2": "|40|88| vs |12|28| / |40|88| vs |28|34| / |40|88| vs |34|40| / |40|88| vs |40|65| / |88|120| vs |12|25| / |88|120| vs |25|28| / |88|120| vs |28|65|",
    "pTj1 vs pTj2": "|-100.0|30.0| vs |-100.0|30.0| / |30.0|10000.0| vs |-100.0|30.0| / |30.0|80| vs |30.0|50| / |80|10000| vs |30.0|50| / |30.0|10000| vs |50|10000|",
    "Nj vs pT4l": "|0|0.99| vs |0|12| / |0|0.99| vs |12|18| / |0|0.99| vs |18|24| / |0|0.99| vs |24|32| / |0|0.99| vs |32|46| / |0|0.99| vs |46|10000| / |1|1.99| vs |0|45| / |1|1.99| vs |45|65| / |1|1.99| vs |65|100| / |1|1.99| vs |100|10000| / |2|100| vs |0|155| / |2|100| vs |155|10000|",
    "pT4l vs pTHj": "|0.0|10000.0| vs |-100.0|0.0| / |0|45| vs |0|50| / |45|70| vs |0|50| / |70|95| vs |0|50| / |95|10000| vs |0|50| / |0|175| vs |50|10000| / |175|10000| vs |50|10000|",
    "TCjmax vs pT4l": "|-100.0|0.0| vs |0.0|10000.0| / |0|30| vs |0|35| / |0|30| vs |35|55| / |0|30| vs |55|70| / |0|30| vs |70|90| / |0|30| vs |90|125| / |0|30| vs |125|10000| / |30|10000| vs |0|250| / |30|10000| vs |250|10000|",
    "absdetajj vs mjj": '|-100|0| vs |-100|0| / |0|3| vs |0|10000| / |3|10| vs |0|450| / |3|10| vs |450|10000|',

    ## HIG 24 013 ##
    #'pT4l': '|0|30|80|200|10000|',
    #'rapidity4l': '|0.0|0.15|0.3|0.6|0.9|2.5|',

}

def binning(var):
    obsBins_input = BINS[var]
    if not 'vs' in obsBins_input: #It is not a double-differential analysis
        obs_bins = {0:(obsBins_input.split("|")[1:(len(obsBins_input.split("|"))-1)]),1:['0','inf']}[obsBins_input=='inclusive']
        obs_bins = [float(i) for i in obs_bins] #Convert a list of str to a list of float
        doubleDiff = False
        print ('It is a single-differential measurement, binning', obs_bins)
    else: #It is a double-differential analysis
        doubleDiff = True
        # The structure of obs_bins is:
        # index of the dictionary is the number of the bin
        # [obs_bins_low, obs_bins_high, obs_bins_low_2nd, obs_bins_high_2nd]
        # The first two entries are the lower and upper bound of the first variable
        # The second two entries are the lower and upper bound of the second variable
        if obsBins_input.count('vs')==1 and obsBins_input.count('/')>=1: #Situation like this one '|0|1|2|3|20| vs |0|10|20|45|90|250| / |0|10|20|80|250| / |0|20|90|250| / |0|25|250|'
            obs_bins_tmp = obsBins_input.split(" vs ") #['|0|1|2|3|20|', '|0|10|20|45|90|250| / |0|10|20|80|250| / |0|20|90|250| / |0|25|250|']
            obs_bins_1st = obs_bins_tmp[0].split('|')[1:len(obs_bins_tmp[0].split('|'))-1] #['0', '1', '2', '3', '20']
            obs_bins_1st = [float(i) for i in obs_bins_1st] #Convert a list of str to a list of float
            obs_bins_tmp = obs_bins_tmp[1].split(' / ') #['|0|10|20|45|90|250|', '|0|10|20|80|250|', '|0|20|90|250|', '|0|25|250|']
            obs_bins_2nd = {}
            for i in range(len(obs_bins_tmp)): #At the end of the loop -> obs_bins_2nd {0: ['0', '10', '20', '45', '90', '250'], 1: ['0', '10', '20', '80', '250'], 2: ['0', '20', '90', '250'], 3: ['0', '25', '250']}
                obs_bins_2nd[i] = obs_bins_tmp[i].split('|')[1:len(obs_bins_tmp[i].split('|'))-1]
                obs_bins_2nd[i] = [float(j) for j in obs_bins_2nd[i]] #Convert a list of str to a list of float
            obs_bins = {}
            k = 0 #Bin index
            for i in range(len(obs_bins_1st)-1):
                for j in range(len(obs_bins_2nd[i])-1):
                    obs_bins[k] = []
                    obs_bins[k].append(obs_bins_1st[i])
                    obs_bins[k].append(obs_bins_1st[i+1])
                    obs_bins[k].append(obs_bins_2nd[i][j])
                    obs_bins[k].append(obs_bins_2nd[i][j+1])
                    k +=1
        elif obsBins_input.count('vs')>1 and obsBins_input.count('/')>1: #Situation like this one '|50|80| vs |10|30| / |50|80| vs |30|60| / |80|110| vs |10|25| / |80|110| vs |25|30|'
            obs_bins_tmp = obsBins_input.split(' / ') #['|50|80| vs |10|30|', '|50|80| vs |30|60|', '|80|110| vs |10|25|', '|80|110| vs |25|30|']
            obs_bins_1st={}
            obs_bins_2nd={}
            obs_bins={}
            for i in range(len(obs_bins_tmp)): #At the end of the loop -> obs_bins_1st {0: ['50', '80'], 1: ['50', '80'], 2: ['80', '110'], 3: ['80', '110']} and obs_bins_2nd {0: ['10', '30'], 1: ['30', '60'], 2: ['10', '25'], 3: ['25', '30']}
                obs_bins_tmp_bis = obs_bins_tmp[i].split(' vs ')
                obs_bins_1st[i] = obs_bins_tmp_bis[0].split('|')[1:len(obs_bins_tmp_bis[0].split('|'))-1]
                obs_bins_1st[i] = [float(j) for j in obs_bins_1st[i]] #Convert a list of str to a list of float
                obs_bins_2nd[i] = obs_bins_tmp_bis[1].split('|')[1:len(obs_bins_tmp_bis[1].split('|'))-1]
                obs_bins_2nd[i] = [float(j) for j in obs_bins_2nd[i]] #Convert a list of str to a list of float
                obs_bins[i] = []
                obs_bins[i].append(obs_bins_1st[i][0])
                obs_bins[i].append(obs_bins_1st[i][1])
                obs_bins[i].append(obs_bins_2nd[i][0])
                obs_bins[i].append(obs_bins_2nd[i][1])
        elif obsBins_input.count('vs')==1 and obsBins_input.count('/')==0: #Situation like this one '|0|1|2|3|20| vs |0|10|20|45|90|250|'
            obs_bins_tmp = obsBins_input.split(" vs ") #['|0|1|2|3|20|', '|0|10|20|45|90|250|']
            obs_bins_1st = obs_bins_tmp[0].split('|')[1:len(obs_bins_tmp[0].split('|'))-1] #['0', '1', '2', '3', '20']
            obs_bins_1st = [float(i) for i in obs_bins_1st] #Convert a list of str to a list of float
            obs_bins_2nd = obs_bins_tmp[1].split('|')[1:len(obs_bins_tmp[1].split('|'))-1] #['0', '10', '20', '45', '90', '250']
            obs_bins_2nd = [float(i) for i in obs_bins_2nd] #Convert a list of str to a list of float
            obs_bins = {}
            k = 0 #Bin index
            for i in range(len(obs_bins_1st)-1):
                for j in range(len(obs_bins_2nd)-1):
                    obs_bins[k] = []
                    obs_bins[k].append(obs_bins_1st[i])
                    obs_bins[k].append(obs_bins_1st[i+1])
                    obs_bins[k].append(obs_bins_2nd[j])
                    obs_bins[k].append(obs_bins_2nd[j+1])
                    k +=1
        else:
            print ('Problem in the definition of the binning')
            quit()
        print ('It is a double-differential measurement, binning for the 1st variable', obs_bins_1st, 'and for the 2nd variable', obs_bins_2nd)
        print (obs_bins)
    return obs_bins, doubleDiff

def binning_v2(var):
    obs_bins, doubleDiff = binning(var)
    return obs_bins
