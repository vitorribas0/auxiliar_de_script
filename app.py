import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
engine = create_engine('sqlite:///jobs_and_scripts.db')
Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    script = Column(Text, nullable=False)

class Script(Base):
    __tablename__ = 'scripts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Função para pesquisar jobs
def search_jobs(search_job_title, search_job_description):
    session = Session()
    job_query = session.query(Job)
    if search_job_title:
        job_query = job_query.filter(Job.title.contains(search_job_title))
    if search_job_description:
        job_query = job_query.filter(Job.description.contains(search_job_description))
    jobs = job_query.all()
    session.close()
    return jobs

# Função para pesquisar scripts
def search_scripts(search_language, search_title):
    session = Session()
    script_query = session.query(Script)

    if search_language != "Todos":
        script_query = script_query.filter(Script.language == search_language)
    if search_title:
        script_query = script_query.filter(Script.title.contains(search_title))

    scripts = script_query.all()
    session.close()
    return scripts

# Menu na sidebar
menu = st.sidebar.selectbox("Menu", ["Adicionar Job", "Adicionar Script", "Pesquisar"])

if menu == "Adicionar Job":
    st.title("Adicionar Novo Job")
    job_title = st.text_input("Título do Job")
    job_description = st.text_area("Breve Descrição")
    job_script = st.text_area("Script")

    if st.button("Salvar Job"):
        session = Session()
        new_job = Job(title=job_title, description=job_description, script=job_script)
        session.add(new_job)
        session.commit()
        st.success("Job salvo com sucesso!")
        session.close()

elif menu == "Adicionar Script":
    st.title("Adicionar Novo Script")
    script_language = st.selectbox("Linguagem", ["Python", "JavaScript", "Java", "C++", "Outros"])
    script_title = st.text_input("Título do Script")
    script_content = st.text_area("Conteúdo")

    if st.button("Salvar Script"):
        session = Session()
        new_script = Script(language=script_language, title=script_title, content=script_content)
        session.add(new_script)
        session.commit()
        st.success("Script salvo com sucesso!")
        session.close()

elif menu == "Pesquisar":
    st.title("Pesquisar")
    search_type = st.radio("Pesquisar por", ["Job", "Script"])
    
    if search_type == "Job":
        search_job_title = st.text_input("Pesquisar por Título do Job")
        search_job_description = st.text_input("Pesquisar por Descrição do Job")

        if st.button("Pesquisar Job"):
            jobs = search_jobs(search_job_title, search_job_description)

            if jobs:
                for job in jobs:
                    st.subheader(f"{job.title}")
                    st.write(f"**Descrição:** {job.description}")
                    st.code(job.script)
            else:
                st.write("Nenhum resultado encontrado.")

    elif search_type == "Script":
        search_script_language = st.selectbox("Pesquisar por Linguagem", ["Todos", "Python", "Pyspark", "Pandas", "SQL", "AWS", "ATHENA", "Sagemaker", "S3"])
        search_script_title = st.text_input("Pesquisar por Título do Script")

        if st.button("Pesquisar Script"):
            scripts = search_scripts(search_script_language, search_script_title)

            if scripts:
                for script in scripts:
                    st.subheader(f"{script.title} ({script.language})")
                    st.code(script.content)
            else:
                st.write("Nenhum resultado encontrado.")
