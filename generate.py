try:
    from PIL import Image
except ImportError:
    import Image
import sys
import os
import random

#local directories for assets
base = r"C:\Users\Stephen\Documents\Saturna\dev\generative_nft\images\\"
head_dir = base+"head\\"
bg_dir = base+"bg\\"
mouth_dir = base+"mouth\\"
nose_dir = base+"nose\\"
eye_dir = base+"eye\\"
bg_s_dir = base+"bg_special\\"

#Dictionaries (index : asset name)
bg_names = {
    1: "Cherry",
    2: "Mint",
    3: "Morning",
    4: "Royal",
    5: "Sunflower",
    6: "Peach",
    7: "Bleak",
    8: "Rosé"
}

head_names = {
    1: "Circle",
    2: "Vertical Oval",
    3: "Horizontal Oval",
    4: "Square",
    5: "Diamond",
    6: "Pointoid"
}

eye_names = {
    1: "Chillin",
    2: "Buggin",
    3: "Bloodshot",
    4: "Third Eye Closed",
    5: "Official Shades",
    6: "Mad Scientist Goggles",
    7: "Wink",
    8: "Proper Sunglasses",
    9: "Third Eye Opened",
    10: "Poison",
    11: "Internet Goggles"
}

mouth_names = {
    1: "Slight Smirk",
    2: "Bad Time",
    3: "Content",
    4: "Picture Day",
    5: "Cheeky",
    6: "Venomous"
}

nose_names = {
    1: "Dot",
    2: "Nostrils",
    3: "Angled",
    4: "Rounded",
    5: "Squiddish"
}

def disp(arr,n):
    s = "["
    for x in arr:
        s+=str(float(x/n))+", "
    s=s[:-2]
    s+="]"
    return s

def getAttributes(bgs,heads,eyes,nose,mouths,seed):
    random.seed(seed)
    bg_idx = random.randint(1,len(bgs))
    head_idx = random.randint(1,len(heads))
    
    icp_goggle = random.randint(1,100)
    if icp_goggle % 5 == 0 and icp_goggle % 3 == 0 and icp_goggle % 2 == 0:
        eyes_idx = 11
    else:
        eyes_idx = random.randint(1,len(eyes)-1)
    
    nose_idx = random.randint(1,len(nose))
    mouth_idx = random.randint(1,len(mouths))
    
    return (bg_idx,head_idx,eyes_idx,nose_idx,mouth_idx)
    
bgs = [0,0,0,0,0,0,0,0]
heads = [0,0,0,0,0,0]
eyes = [0,0,0,0,0,0,0,0,0,0,0]
nose = [0,0,0,0,0]
mouths = [0,0,0,0,0,0]
generated = set()

def generate(j,seed):
    #os.remove("*.png")
    random.seed(seed)
    specialPercent=0
    while len(generated) < j:
        generated.add(getAttributes(bgs,heads,eyes,nose,mouths,int(seed)+random.randint(0,10000926234632452345)))
    
    #print(generated)
    for i in range(1,j+1):
        attributes = list(generated.pop())
        #print(attributes)
        bgs[attributes[0]-1]+=1
        heads[attributes[1]-1]+=1
        eyes[attributes[2]-1]+=1
        nose[attributes[3]-1]+=1
        mouths[attributes[4]-1]+=1
        
        special = random.randint(0,1000)%5 == 0 and random.randint(0,1000)%3 == 0
        if special:
            b_dir = bg_s_dir+str(attributes[0])+".png"
            specialPercent+=1
        else:
            b_dir = bg_dir+str(attributes[0])+".png"
        b = Image.open(b_dir).convert("RGBA")
        
        h_dir = head_dir+str(attributes[1])+".png"
        
        h = Image.open(h_dir).convert("RGBA")
        
        e_dir = eye_dir+str(attributes[2])+".png"
        e = Image.open(e_dir).convert("RGBA")
        
        n_dir = nose_dir+str(attributes[3])+".png"
        n = Image.open(n_dir).convert("RGBA")
        
        m_dir = mouth_dir+str(attributes[4])+".png"
        m = Image.open(m_dir).convert("RGBA")
        
        bh = Image.alpha_composite(b,h)
        bh.save("bh.png","PNG")
        
        bh_new = Image.open("bh.png").convert("RGBA")
        bhn = Image.alpha_composite(bh_new,n)
        bhn.save("bhn.png","PNG")
        bhn_new = Image.open("bhn.png").convert("RGBA")
        
        bhne = Image.alpha_composite(bhn_new,e)
        bhne.save("bhne.png","PNG")
        bhne_new = Image.open("bhne.png").convert("RGBA")
        bhnem = Image.alpha_composite(bhne_new,m)
        bhnem = bhnem.resize((1000,1000),Image.NEAREST)
        outstring = ""
        outstring = "Image "+str(i)+" has attributes: ["+bg_names[attributes[0]]+", "+head_names[attributes[1]]+", "+eye_names[attributes[2]]+", "+nose_names[attributes[3]]+", "+mouth_names[attributes[4]]+"]"
        if special:
            outstring+=" *SPECIAL* "
        print(outstring)
        bhnem.save("nft_"+str(i)+".png","PNG")
        os.remove("bh.png")
        os.remove("bhne.png")
        os.remove("bhn.png")
    print("*************************************")
    print("Final Attribute Distribution: ")
    print("Backgrounds: "+disp(bgs,j))
    print("Heads: "+disp(heads,j))
    print("Eyes: "+disp(eyes,j))
    print("Nose: "+disp(nose,j))
    print("Mouths: "+disp(mouths,j))
    print("Special Background ratio: ",str(specialPercent/j))

def main(j,seed):
    generate(j,seed)
    
if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) <= 2:
        print("Error: Not enough arguments")
    else:
        main(int(sys.argv[1]),int(sys.argv[2]))