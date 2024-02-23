import pandas as pd
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys

def generate_word_cloud(file_name, output_file_name):
    start_time = time.time()

    print("Reading WhatsApp texts at %s seconds." % (time.time() - start_time))
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.readlines()
    except FileNotFoundError:
        print("\n\nIncorrect file name. Recheck.")
        sys.exit(1)

    # Extract timestamp and message from each line
    timestamps = [line[:18] for line in data]
    messages = [line[21:].strip() if len(line) > 21 else "" for line in data]

    # Create a DataFrame with extracted data
    df = pd.DataFrame({'Timestamp': timestamps, 'Message': messages})

    print("Generating pandas dataframe from text file at %s seconds." % (time.time() - start_time))

    # Remove lines containing "image omitted"
    df = df[~df['Message'].str.contains("image omitted")]
    text = df['Message'].to_string()

    contact_name1 = "" #enter person1 name
    text_person_1 = df[df['Message'].str.contains(contact_name1)]['Message'].to_string()
    contact_name2 = "" #enter person2 name
    text_person_2 = df[df['Message'].str.contains(contact_name2)]['Message'].to_string()

    # Remove occurrences of specific words from the text
    words_to_remove = ["Voice call"]
    for word in words_to_remove:
        text = text.replace(word, '')
        text_person_1 = text_person_1.replace(word, '')
        text_person_2 = text_person_2.replace(word, '')

    #re-extraction of text to remove contact name from message too.
    text = ''.join(line.split(']')[1].split(':')[1] if ']' in line and ':' in line else line for line in text.split('\n'))
    text_person_1 = ''.join(line.split(']')[1].split(':')[1] if ']' in line and ':' in line else line for line in text_person_1.split('\n'))
    text_person_2 = ''.join(line.split(']')[1].split(':')[1] if ']' in line and ':' in line else line for line in text_person_2.split('\n'))
    

    print("Generating word cloud at %s seconds." % (time.time() - start_time))

    # Generate word cloud for overall text
    wc = WordCloud(
        background_color='white',
        stopwords=STOPWORDS,
        width=1920,
        height=1080,
        max_words=500,
    )
    wordcloud_image = wc.generate(text)

    # Generate word cloud for individual's text
    wc_person_1 = WordCloud(
        background_color='white',
        stopwords=STOPWORDS,
        width=1920,
        height=1080,
        max_words=500,
    )
    wc_person_2 = WordCloud(
        background_color='white',
        stopwords=STOPWORDS,
        width=1920,
        height=1080,
        max_words=500,
    )
    wordcloud_image_person_1 = wc_person_1.generate(text_person_1)
    wordcloud_image_person_2 = wc_person_2.generate(text_person_2)

    # This will save the word clouds to png images. You can change the names as you
    # see fit.
    print("Saving word cloud images at %s seconds." % (time.time() - start_time))
    wordcloud_image.to_file(output_file_name)
    wordcloud_image_person_1.to_file("person1_word_cloud.png")
    wordcloud_image_person_2.to_file("person2_word_cloud.png")

    # Display the word clouds
    print("Displaying word cloud images at %s seconds." % (time.time() - start_time))
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(wordcloud_image, interpolation='bilinear')
    axes[0].axis("off")
    axes[0].set_title('Overall Word Cloud')

    axes[1].imshow(wordcloud_image_person_1, interpolation='bilinear')
    axes[1].axis("off")
    axes[1].set_title('person1 Word Cloud')

    axes[2].imshow(wordcloud_image_person_2, interpolation='bilinear')
    axes[2].axis("off")
    axes[2].set_title('person2 Word Cloud')

    plt.show()

if __name__ == "__main__":
    text_file_name = "chat.txt" #replace with file name of the whatsapp exported chat
    output_file_name = "word_cloud.png"
    generate_word_cloud(text_file_name, output_file_name)
