import streamlit as st
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

st.title("Book Recommendation System")

# Define index page
if st.sidebar.button("Home", key='1'):
    st.write(
        "## Welcome to Book Recommendation System",
        "Explore popular books and find recommendations based on your input."
    )
    st.write("### Popular Books:")
    st.dataframe(popular_df)

# Define recommendation page
if st.sidebar.button("Recommend", key='2'):
    st.write(
        "## Book Recommendation",
        "Enter a book title to get recommendations:"
    )
    user_input = st.text_input("Enter Book Title:")
    if st.button("Recommend"):
        try:
            # Search for the index of the user input in the pt index
            index = np.where(pt.index == user_input)[0][0]
            
            # Sort similar items by similarity score
            similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title']==pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(item)

            # Display recommendations
            st.write("### Recommendations:")
            for item in data:
                st.write(item)
        except IndexError:           
            st.error("Book not found. Please enter a valid book title.")

# Run the app
if __name__ == "__main__":
    st.sidebar.title("")
