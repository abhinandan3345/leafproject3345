import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
        
local_css("style.css")

# ---- HEADER SECTION ----

model = load_model('leaf_model.h5')
labels = {0: 'Aam', 1: 'Amrud', 2: 'Annar', 3: 'Arhul', 4:'Chandan', 5: 'Chandni', 6: 'Curry', 7: 'Drumstick', 8: 'Ghrit Kumari', 9: 'Giloy', 10: 'Harive-Dantu', 11: 'Jackfruit', 12:'Jamaica Cherry' , 13:'Jamun' , 14: 'Karanda', 15:'Karanja' , 16:'Malabar spinach' , 17:'Mithi', 18:'Mogra', 19:'Neem',20:'Nimbu', 21:'Oleander', 22:'Paan' , 23:'Parijata', 24: 'Peepal', 25: 'Phagoora', 26: 'Pudina', 27: 'Rasna', 28: 'Rose Apple', 29: 'Sarso', 30: 'Tindora',31: 'Tulsi'}  

      
dir1={'Aam':'The extract of mango leaves have been used for a long time to cure asthma and it is believed that they are effective in treating diabetes. The leaves contain an abundance of nutrients. These greens are packed with pectin, fiber and vitamin C, which can be beneficial in controlling the blood sugar level.',
'Amrud':'Guava or amrud is a Vitamin C-rich fruit with lots of antioxidants, potassium and fibre. Eating guava every day can be beneficial for your blood sugar levels, heart health, digestive system and also weight loss',
'Annar':'Besides aiding in fat loss, pomegranate leaves are found to be useful in treating a number of disorders and ailments, such as insomnia, abdominal pain, dysentery, cough, jaundice, mouth ulcers, skin ageing, and inflammation of the skin like eczema',
'Arhul':'This plant has various important medicinal uses for treating wounds, inflamation, fever and coughs, diabetes, infections caused by bacteria and fungi, hair loss, and gastric ulcers in several tropical countries.',
'Chandan':'White sandalwood is used for treating the common cold, cough, bronchitis, fever, and sore mouth and throat. It is also used to treat urinary tract infections (UTIs), liver disease, gallbladder problems, heatstroke, gonorrhea, headache, and conditions of the heart and blood vessels (cardiovascular disease).',
'Chandni':'Apart from its pretty status, Chandni has a spot created in Ayurveda medicine too — for dental caries, for scabies,as cough medicine and for eye ailments (like burning sensation). Its a plant that requires full to partial sunlight, any soil, moist environments, but not waterlogged roots as it will then breed pests',
'Curry':'Curry leaves are a rich source of vitamin A, vitamin B, vitamin C, vitamin B2, calcium, and iron, apart from a heavy distinctive odor and pungent taste. It helps in the treatment of dysentery, diarrhea, diabetes, morning sickness, and nausea by adding curry leaves to your meals',
'Drumstick':'High on vitamin C and antioxidants, drumstick helps to combat against common cold, flu and stave off several common infections. The anti-inflammatory and anti-bacterial properties of drumstick assists in lessening the symptoms of asthma, cough, wheezing and other respiratory problems.16',
'Ghrit Kumari':'Aloe vera gel is often used on the skin to treat sunburn, burns, and eczema. It has a soothing effect that may aid in treating symptoms caused by genital herpes, poison oak, poison ivy, and skin irritation in people treated with radiation.',
'Giloy':'also known as Amrita or Guduchi in Hindi, is an herb that helps improve digestion and boost immunity. It has heart-shaped leaves that resemble betel leaves. All parts of the plant are used in Ayurvedic medicine. However, the stem is thought to have the most beneficial compounds.',
'Harive-Dantu':'Used mostly as part of the winter dishes of saag, it is the less favourite relative of spinach. But Amaranth leaves are much superior to most greens because they are a powerhouse of nutrients. Let us look at some health benefits of eating Amaranth leaves.',
'Jackfruit':'They may help prevent diseases like cancer and heart disease, as well as eye problems like cataracts and macular degeneration. As a jackfruit ripens, its carotenoid levels may go up. Jackfruit also contains many other antioxidants that can help delay or prevent cell damage in your body',
'Jamaica Cherry':'he fruits are commonly called Jamaican cherry and are red in colour. The flowers are used as an antiseptic and to treat abdominal cramps and spasms. It is also taken to relieve headaches and colds. Muntingia calabura fruits possess antioxidant property.',
'Jamun':'The high alkaloid content present in jamun is effective in controlling hyperglycaemia or high blood sugar. Apart from the fruit, extracts from the seeds, leaves and bark are useful for reducing the high levels of blood sugar in your body.',
'Karanda':'Its fruit is used in the ancient Indian herbal system of medicine, Ayurvedic, to treat acidity, indigestion, fresh and infected wounds, skin diseases, urinary disorders and diabetic ulcer, as well as biliousness, stomach pain, constipation, anemia, skin conditions, anorexia and insanity.',
'Karanja':'Karanja is medicinal herb mainly used for skin disorders. Karanja is widely used in managing constipation.used for piles due to anti-inflammatory properties.Karanja oil is mainly applied on the skin to manage boils and eczema as well as heal wounds due to its Ropan (healing) and antimicrobial property.',
'Malabar spinach':' Malabar spinach is a well known nutritious vegetable and a natural coolant. It nourishes, makes the body stout, purifies blood, rejuvenates and acts as aphrodisiac. Including it in regular diet helps to prevent weakness of bones, anemia, cardiovascular diseases and cancers of colon',
'Mithi':'Fenugreek is taken by mouth for digestive problems such as loss of appetite, upset stomach, constipation, inflammation of the stomach (gastritis). Fenugreek is also used for diabetes, painful menstruation, polycystic ovary syndrome, and obesity',
'Mogra':'They tend to reduce stress and depression just by being in an area near you. It was also used as a medicine in the earlier days because it can heal wounds. Another way it alleviates pain is by reducing headaches and backaches. Its oils are still used in massage therapies that can help aid arthritis.',
'Neem':'Neem is used for leprosy, eye disorders, bloody nose, intestinal worms, stomach upset, loss of appetite, skin ulcers, diseases of the heart and blood vessels (cardiovascular disease), fever, diabetes, gum disease (gingivitis), and liver problems. The leaf is also used for birth control and to cause abortions.',
'Nimbu':'Lemons contain about 31 grams of Vitamin C, which is nearly double the amount of Vitamin C needed in your daily diet. Along with boosting immunity, this burst of Vitamin C can reduce your risk of stroke and heart disease with regular consumption.',
'Oleander':'Despite the danger, oleander seeds and leaves are used to make medicine. Oleander is used for heart conditions, asthma, epilepsy, cancer, painful menstrual periods, leprosy, malaria, ringworm, indigestion, and venereal disease; and to cause abortions',
'Paan':'It is most commonly used to treat chronic bronchitis, asthma, constipation, gonorrhea, paralysis of the tongue, diarrhea, cholera, chronic malaria, viral hepatitis, respiratory infections, stomachache, bronchitis, diseases of the spleen, cough, and tumors.',
'Parijata':'Parijat leaves provide various beneficial health effects due to the presence of anti-bacterial, anti-inflammatory, antipyretic (fever controlling) and anthelmintic (parasitic worm expeller) properties. Studies suggest that Parijat leaves also have anti-asthmatic and anti-allergic properties.',
'Peepal':'Leaves have been traditionally used in the treatment of heart ailments, nose bleeding, diabetes, constipation, fever, jaundice, etc. You can take some extract of 2-3 leaves of Peepal tree and mix it with water and little sugar, taking this mix twice a day can help in relieving symptoms of jaundice.',
'Phagoora':'Roasted figs are taken for diarrhea and dysentery. Root latex is used in mumps, cholera, diarrhea and vomiting. Several tribes in Northern eastern India especially in Manipur use the leaf of Ficus auriculata, traditionally for the treatment of diabetes.',
'Pudina':'Contains menthol that can help relax muscles and ease the pain. Applying pudina juice on your forehead and temples can give you relief from headache. Also, balms of pudina base or mint oil are effective in curing headaches.',
'Rasna':'Rasna is a herb mentioned in Ayurveda for the treatment of pain, indigestion, gout, cough and general debility. Vanda roxburghii and Alpinia galanga is also taken as Rasna in Bengal and South India respectively. Latin name- Pluchea lanceolata C.B Clarke. Family- Asteraceae.',
'Rose apple':'Rose apple is good for pregnant women as it fulfills iron and vitamin deficiency in the body. Its seed and leaves are used for treating asthma and fever. Rose apples improve brain health and increase cognitive abilities. They are also effective against epilepsy, smallpox and inflammation in joints',
'Sarso':'It is a folk remedy for arthritis, foot ache, lumbago and rheumatism. Brassica juncea is grown mainly for its seed used in the fabrication of brown mustard or for the extraction of vegetable oil. Brown mustard oil is used against skin eruptions and ulcers.',
'Tindora':'Ivy gourd is most often used for diabetes. People also use ivy gourd for gonorrhea, constipation, wounds, and other conditions, but there is no good scientific evidence to support these uses. Ivy gourd fruit and leaves are also used as a vegetable in India and other Asian countries.',
'Tulsi':'Tulsi most popularly known as Tulsi has been used for thousands of years in Ayurveda for its diverse healing properties. Healing Power: The Basil or Tulsi plant has many medicinal properties. The leaves strengthen the stomach and help in respiratory diseases.'}


def processed_img(img_path):
    img=load_img(img_path,target_size=(128,128,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()



def fetch_name(prediction):
    try:
        URL = "https://www.google.com/search?q=scientific+name of"  + prediction
        headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }
        page = requests.get(URL,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find(class_='Z0LcW').get_text()
        return name
    except Exception as e: 
        st.error("Can't fetch the Scientific Name")
        print(e)


def run():
    st.title("Automatic Identification Of Ayurvedic Leaves Using Deep Learning")
    st.header("Please Check The Sample Of Leaves In Saved Images Folder")
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250,250))
        st.image(img,use_column_width=False)
        save_image_path = r'C:\LeafProject\SavedImages\Images'+img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())
            
           
            
             
          
        if img_file is not None:
            result= processed_img(save_image_path)
            st.success("**Predicted : "+result+'**')
        na = fetch_name(result)
        
        if na:
            st.warning('**Scientific Name:' +na+'**')
        for na in dir1:
            if na == result:
                st.info('**Benifits : '+ dir1.get(na)+'**')
         
            
            
                
run()                    
                    
                #continue
                    #break

                
#     except Exception as e:
        
#         st.error("Can't fetch the Scientific Name")
#         print(e)         
            #if na == dir1[na]:
                
                #st.info('**Benifits : '+ dir1.get(na)+'**')
             #   else :
              #  print("Sorry We Can't fetch.......")
            
#                         if na in dir1 :
#                         st.info('**Benifits : '+ dir1.get(na)+'**')
#         else:
#                         print("Sorry We Can't fetch.......")
