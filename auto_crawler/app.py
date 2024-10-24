import streamlit as st
import threading
from queue import Queue
from spider import Spider
from domain import get_domain_name
from general import file_to_set, set_to_file

PROJECT_NAME = 'crawled_data'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
queue = Queue()

st.title("Automated Web Crawler Tool")
homepage = st.text_input("Enter the homepage URL to start crawling:")
num_threads = st.slider("Select the number of threads:", 1, 20, 8)

if st.button("Start Crawling"):
    if homepage:
        domain_name = get_domain_name(homepage)
        Spider(PROJECT_NAME, homepage, domain_name)

        def create_workers():
            for _ in range(num_threads):
                t = threading.Thread(target=work)
                t.daemon = True
                t.start()

        def work():
            while True:
                url = queue.get()
                Spider.crawl_page(threading.current_thread().name, url)
                queue.task_done()

        def create_jobs():
            for link in file_to_set(QUEUE_FILE):
                queue.put(link)
            queue.join()

        create_workers()
        create_jobs()
        st.success("Crawling completed!")

        crawled_links = file_to_set(CRAWLED_FILE)
        st.write("Crawled Links:")
        st.write(crawled_links)

        download_file = f"{PROJECT_NAME}/crawled_links.csv"
        set_to_file(crawled_links, download_file)

        with open(download_file, "rb") as f:
            st.download_button(
                label="Download Crawled Links as CSV",
                data=f,
                file_name="crawled_links.csv",
                mime="text/csv"
            )
    else:
        st.error("Please enter a valid homepage URL.")
