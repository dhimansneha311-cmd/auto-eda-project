import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Auto EDA", layout="wide", page_icon="🐍" )
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #eef2f7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1e293b;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Main Title */
h1 {
    color: #0f172a;
    text-align: center;
    font-size: 50px !important;
    font-weight: bold;
}

/* Subheaders */
h2, h3 {
    color: #1e293b;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px;
    font-size: 16px;
}

/* Download Button */
.stDownloadButton>button {
    background-color: green;
    color: white;
    border-radius: 12px;
    border: none;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: white;
    border: 2px solid #dbeafe;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 class='main-title'>AUTO EDA PROJECTS</h1>",
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([1,1,1])
with col2:
  st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
           width=150)
st.sidebar.title("Auto EDA Navigation")
option = st.sidebar.radio("Select Option",
                          [
                             "Overview",
                             "Visualization",
                             "Cleaning"
                          ])

uploader = st.file_uploader(label="upload your csv file", type=["csv"])

if uploader is not None:
    data=pd.read_csv(uploader)
    st.subheader("All Data")
    rows=st.slider("Select Number Of Rows",
                   min_value=5,
                   max_value=100,
                   value=10)
    st.dataframe(data.head(rows))

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Total Rows", data.shape[0])
    col2.metric("Total Columns", data.shape[1])
    col3.metric("Missing Values", data.isnull().sum().sum())
    col4.metric("Duplicated Values", data.duplicated().sum())

    
    if option == "Overview":
       st.header("Overview of dataset")
       st.subheader("All Information About Data")
       if st.checkbox("Shape of Dataset"):
        st.write("Rows :",data.shape[0])
        st.write("Columns :",data.shape[1])

       search_col = st.selectbox("Search Any Column",
                                 data.columns)
       st.write("Selected Column Data")
       st.write(data[search_col])
       if st.checkbox("Columns Name"):
        st.write(data.columns)

       if st.checkbox("Data Types"):
        st.write(data.dtypes)

if option == "Cleaning":
   st.header("Data Cleaning")
   if st.checkbox("Check Duplicates"):
    st.write("Duplicates :",data.duplicated().sum())
   if st.button("Remove Duplicates"):
     data.drop_duplicates(inplace=True)
     st.success("Duplicates Remove Successfully")

   if st.checkbox("Statistics"):
      st.write(data.describe())
      numeric_data = data.select_dtypes(include="number")
      fig, ax = plt.subplots(figsize=(10,5))
      sns.heatmap(
      numeric_data.corr(),
      annot=True,
      cmap="coolwarm",
      ax=ax
     )
      st.pyplot(fig)

   if st.checkbox("Check Null Values"):
     missing = data.isnull().sum()
     st.write(missing[missing>0])

     st.subheader("Null Values Percentage")
     per = (missing/len(data))*100
     st.write(per[per>0])
               
   if st.checkbox("Handling Missing Values"):
     for i in per.index:
      if per[i]>10:
       data.drop(i, axis=1, inplace=True)
      else:
        if data[i].dtype=="str":
         data.dropna(inplace=True)
        else:
         data[i].fillna(data[i].mean(), inplace=True)
         st.write(data.isnull().sum())
      
   if st.checkbox("Check Unique Values"):
         col = st.selectbox(
                     "Select Column",
                        data.columns
                   )

         st.write("Unique Values :")
         st.write(data[col].unique())
         st.write("Value Counts :")
         st.write(data[col].value_counts())


   if st.checkbox("Download Cleaned Data"):
    csv = data.to_csv(index = False).encode("utf-8")
    st.download_button(label = "Download CSV file",
                      data = csv,
                      file_name = "Cleaned_data.csv",
                      mime= "text/csv")

if option == "Visualization":
   st.header("Visualization")

   if st.checkbox("Histogram"):
    numeric_col = data.select_dtypes(include="number").columns
    col = st.selectbox("Select Numerical Column", numeric_col)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(data[col], kde=True, ax=ax)
    st.pyplot(fig)

   if st.checkbox("Boxplot"):
    numeric_col = data.select_dtypes(include="number").columns
    col =  st.selectbox("Select olumn fox boxplot", numeric_col)
    fig,ax = plt.subplots(figsize=(8,5))
    sns.boxplot( x=data[col], ax = ax)
    st.pyplot(fig)

   if st.checkbox("Piechart"):
    cat_col =  data.select_dtypes(include="str").columns
    col = st.selectbox("Select Categorical Columns", cat_col)
    value_count = data[col].value_counts()
    fig,ax = plt.subplots(figsize=(7,7))
    ax.pie(value_count,
          labels=value_count.index,
          autopct="%1.1f%%")
    st.pyplot(fig)

   if st.checkbox("Countplot"):
      cat_col =  data.select_dtypes(include="str").columns
      col = st.selectbox("Select Columns for countplot", cat_col)
      fig,ax = plt.subplots(figsize=(10,5))
      sns.countplot( x= data[col],
                    ax= ax)
      plt.xticks(rotation=45)
      st.pyplot(fig)

   if st.checkbox("Pairplot"):
      numeric_data = data.select_dtypes(include="number")
      pair_fig = sns.pairplot(numeric_data)
      st.pyplot(pair_fig.fig)
    
   if st.checkbox("Scatterplot"):
      numeric_col = data.select_dtypes(include="number").columns
      x_col = st.selectbox("Select x-axis", numeric_col, key="scatter_x")
      y_col = st.selectbox("Select y-axis", numeric_col, key="scatter_y")
      fig,ax = plt.subplots(figsize=(8,5))
      sns.scatterplot( 
        x=data[x_col],
        y=data[y_col],
        ax=ax
      )
      st.pyplot(fig)

   if st.checkbox("Lineplot"):
      numeric_col = data.select_dtypes(include="number").columns
      x_col = st.selectbox("Select x-axis", numeric_col, key="line_x")
      y_col = st.selectbox("Select y-axis", numeric_col, key="line_y")
      fig,ax = plt.subplots(figsize=(8,5))
      sns.lineplot( 
        x=data[x_col],
        y=data[y_col],
        ax=ax
      )
      st.pyplot(fig)


   
st.markdown("""
  <hr>
            <center>
            <h4>Developed By Sneha</h4>
            </h4>
            </center> 
            """, unsafe_allow_html=True)