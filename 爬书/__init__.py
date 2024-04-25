import asyncio
import re
import tkinter as tk
from tkinter import ttk, messagebox
import search_book
import get_bookpage
import threading
from concurrent.futures import ThreadPoolExecutor
def search_books():
    window.title('爬书-搜索结果')
    # 隐藏搜索界面的框架
    search_frame.pack_forget()
    # 显示结果界面的框架
    result_frame.pack(fill='both', expand=True)




    # 清空表格中的内容
    for row in tree.get_children():
        tree.delete(row)

    # 获取输入的书名
    book_name = entry.get()

    # 调用搜索函数，并传递书名参数
    search_results = search_book.search_book(book_name)
    def tree_insert_results_frame(book,author):
        tree.insert('', 'end', values=(author[0], author[1], book))
    # 填充表格
    for book, author in search_results.items():
        p1.submit(tree_insert_results_frame,book, author)


def on_double_click(event):
    item = tree.selection()[0]
    book_name = tree.item(item, "values")[0]
    author = tree.item(item, "values")[1]
    url=tree.item(item, "values")[2]

    # 显示书名和作者信息到bookpage_frame界面
    threading.Thread(target=display_book_details,args=(book_name, author,url)).start()

    # 隐藏结果界面的框架
    result_frame.pack_forget()
    # 显示书籍详情界面的框架
    bookpage_frame.pack(fill='both', expand=True)




def return_to_search_from_result():
    def pool_delete_from_result(row):
        tree.delete(row)
    # 清空结果界面的内容
    for row in tree.get_children():
        p1.submit(pool_delete_from_result,row)
    # 隐藏书籍详情界面的框架
    result_frame.pack_forget()
    # 显示搜索界面的框架
    search_frame.pack()


def return_to_result_from_bookpage():
    # 清空书籍详情界面的内容
    def pool_destroy_boopage_frame(widget):
        widget.destroy()
    for widget in bookpage_frame.winfo_children():
        p1.submit(pool_destroy_boopage_frame,widget)
    # 隐藏书籍详情界面的框架
    bookpage_frame.pack_forget()
    # 显示搜索结果界面的框架
    result_frame.pack(fill='both', expand=True)

def return_to_result_from_pagdetails():
    # 清空书籍详情界面的内容
    def pool_destroy_pagedetails_frame(widget):
        widget.destroy()

    for widget in pagedetails_frame.winfo_children():
        p1.submit(pool_destroy_pagedetails_frame, widget)
    # 隐藏书籍详情界面的框架
    pagedetails_frame.pack_forget()
    # 显示搜索结果界面的框架
    bookpage_frame.pack(fill='both', expand=True)

def create_return_button_for_bookpage():

    def pool_destroy_boopage_frame(widget):
        widget.destroy()

    # Clear existing return button widgets
    for widget in bookpage_frame.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == "返回搜索结果":
            p1.submit(pool_destroy_boopage_frame,widget)
    # Create return button

    return_to_result_button = tk.Button(bookpage_frame, text="返回搜索结果", command=return_to_result_from_bookpage,
                                        width=20, height=2)
    return_to_result_button.pack(side="bottom")


def create_return_button_for_pagedetails():
    def pool_destroy_pagedetails_frame(widget):
        widget.destroy()

    # Clear existing return button widgets
    for widget in pagedetails_frame.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == "返回":
            p1.submit(pool_destroy_pagedetails_frame,widget)
    # Create return button

    return_to_result_button = tk.Button(pagedetails_frame, text="返回", command=return_to_result_from_pagdetails,
                                        width=20, height=2)
    return_to_result_button.pack(side="bottom")

def display_page_details(book_number,page_number,page_name):
    def display_page_content(page_txt):
        page_content.delete('1.0', tk.END)
        page_content.insert(tk.END, page_txt)
    def destrory_pagedetails_frame(widget):
        widget.destroy()

    for widget in pagedetails_frame.winfo_children():
        p1.submit(destrory_pagedetails_frame,widget)
    window.title('爬书-章节内容')
    page_txt_lable=tk.Label(pagedetails_frame, text=f'{page_name}',font=("宋体", 12 ))
    page_txt_lable.pack()
    warn_label = tk.Label(pagedetails_frame, text=f"若未显示内容，请稍等片刻", font=('Arial', 12), fg="red")
    warn_label.pack()
    page_content = tk.Text(pagedetails_frame, wrap=tk.WORD,font=("宋体", 12 ))
    page_content.pack(fill=tk.BOTH, expand=True)
    page_txt =get_bookpage.get_noe_text(book_number,page_number)   # 替换为你的小说章节内容
    get_bookpage.get_noe_text(book_number,page_number)

    display_page_content(page_txt)
    create_return_button_for_pagedetails()


def onbild_page_details(book_details_tree):
    item = book_details_tree.selection()[0]
    page_name = book_details_tree.item(item, "values")[0]
    page_link = book_details_tree.item(item, "values")[1]
    pattern = r"mulu_(\d+)/(\d+)\.html"
    match = re.search(pattern, page_link)
    if match:
        book_number = match.group(1)  # 提取2530
        page_number = match.group(2)  # 提取15174076
    # 显示书名和作者信息到bookpage_frame界面
    threading.Thread(target=display_page_details, args=(book_number,page_number,page_name)).start()

    # 隐藏结果界面的框架
    bookpage_frame.pack_forget()
    # 显示书籍详情界面的框架
    pagedetails_frame.pack(fill='both', expand=True)



def display_book_details(book_name, author,url,page=0):
    # 清空书籍详情界面的内容
    def destrory_bookpage_frame(widget):
        widget.destroy()

    for widget in bookpage_frame.winfo_children():
        p1.submit(destrory_bookpage_frame,widget)
    window.title('爬书-书籍章节')
    # 显示书名和作者信息
    book_label = tk.Label(bookpage_frame, text=f"书名：{book_name}\n{author}", font=('Arial', 12))
    book_label.pack()
    warn_label = tk.Label(bookpage_frame, text=f"若未显示章节或下载，请稍等片刻", font=('Arial', 12),fg="red")
    warn_label.pack()
    page_num = get_bookpage.get_book_page_num(url,p1)  # 每页章节详情，len+1为总页数

    if page < 0:
        page = 0
    elif page >= len(page_num):
        page = len(page_num) - 1
    # 显示当前页数
    current_page_label = tk.Label(bookpage_frame, text=f"当前页数：{page + 1},总页数：{len(page_num)}")
    current_page_label.pack()

    # 创建表格
    book_details_tree = ttk.Treeview(bookpage_frame, columns=( 'Value'), show='headings')

    book_details_tree.heading('Value', text='书籍章节')


    def tree_insert_bookpage_frame(name,link):
        book_details_tree.insert('', 'end', values=(name,link,))
    # 添加书籍属性和值
    page_name_link = p1.submit( get_bookpage.get_page_details,page_num[page]).result() # 获取页面书籍详情信息
    for name, link in page_name_link.items():

        p1.submit(tree_insert_bookpage_frame,name,link)

    # 可以根据需要添加更多属性和值
    book_details_tree.bind("<Double-1>",lambda event:onbild_page_details(book_details_tree))
    book_details_tree.pack(fill='both', expand=True)
    # 创建分页按钮
    create_pagination_buttons(book_name,author,url,page,len(page_num))
    # 创建跳转到指定页数的功能
    create_goto_page_function(book_name, author, url, len(page_num))
    # 创建下载按钮
    create_download_buuton(url,book_name)
    # 添加返回按钮到书籍详情界面
    create_return_button_for_bookpage()
def create_pagination_buttons(book_name, author, url, current_page, total_pages):

    # 创建上一页按钮
    prev_button = tk.Button(bookpage_frame, text='上一页', command=lambda:threading.Thread(target= prev_page,args=(book_name, author, url, current_page, total_pages)).start())
    prev_button.pack(side='left')

    # 创建下一页按钮
    next_button = tk.Button(bookpage_frame, text='下一页', command=lambda: threading.Thread(target=next_page,args=(book_name, author, url, current_page, total_pages)).start())
    next_button.pack(side='left')


def prev_page(book_name, author, url, current_page, total_pages):
    display_book_details(book_name, author, url, current_page - 1)


def next_page(book_name, author, url, current_page, total_pages):
    display_book_details(book_name, author, url, current_page + 1)

def create_goto_page_function(book_name, author, url, total_pages):
    def goto_page():
        try:
            page_num = int(page_input.get()) - 1
            if 0 <= page_num < total_pages:
                threading.Thread(target=display_book_details,args=(book_name, author, url, page_num)).start()
            else:
                messagebox.showerror("错误", f"请输入 1 至 {total_pages} 之间的页码")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的页码")

    # 创建输入框和跳转按钮
    page_input = tk.Entry(bookpage_frame)
    page_input.pack(side='left')
    goto_button = tk.Button(bookpage_frame, text='跳转', command=goto_page)
    goto_button.pack(side='left')

def download_download(url,bookname):

    # 创建顶层窗口作为提示框
    download_dialog = tk.Tk()
    download_dialog.title(f"下载{bookname}")
    download_label = tk.Label(download_dialog, text=f"正在下载{bookname}")
    download_label.pack()
    # 创建进度条
    progress_bar = ttk.Progressbar(download_dialog, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)
    # 设置窗口位置和大小
    download_dialog.geometry("300x100+200+200")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_bookpage.get_link(url=url,book_name=bookname,p1=p1,progress_bar=progress_bar,download_dialog=download_dialog,download_label=download_label))

def thread_download_download(url, bookname):
    threading.Thread(target=download_download, args=(url, bookname,)).start()

def create_download_buuton(url,bookname):
    download_button = tk.Button(bookpage_frame, text='下载', command=lambda: thread_download_download(url,bookname))
    download_button.pack(side='left')
def start_search_books_thread():
    threading.Thread(target=search_books).start()

if __name__ == '__main__':
    p1 = ThreadPoolExecutor(17)
    window = tk.Tk()
    window.geometry('1000x650')
    window.config(highlightthickness=3, highlightbackground="black")
    window.title("爬书-搜索")  # 设置窗口标题为"爬书-搜索"

    search_frame = tk.Frame(window)
    result_frame = tk.Frame(window)
    bookpage_frame = tk.Frame(window)
    pagedetails_frame = tk.Frame(window)

    # 书名搜索界面
    search_label = tk.Label(search_frame, text="请输入需要搜索的书名", width=50, height=5, font=('Arial', 12))
    search_label.pack()

    entry = tk.Entry(search_frame, width=70, highlightcolor='red', font=('Arial', 15))
    entry.pack()

    # 添加搜索按钮
    search_button = tk.Button(search_frame, text="搜索", command=start_search_books_thread, width=20, height=2)
    search_button.pack()

    # 将框架添加到窗口中显示
    search_frame.pack()

    # 结果界面
    result_label = tk.Label(result_frame, text="爬书-搜索结果", width=50, height=5, font=('Arial', 12))
    result_label.pack()

    # 创建表格
    style = ttk.Style()
    style.configure("Treeview", font=('宋体', 14))  # 设置表格字体大小
    tree = ttk.Treeview(result_frame, columns=('Book', 'Author'), show='headings')
    tree.heading('Book', text='书名')
    tree.heading('Author', text='作者')

    # 创建垂直滚动条并与表格关联
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill='both', expand=True)
    scrollbar.pack(side="right", fill="y")

    # 绑定双击事件
    tree.bind("<Double-1>",on_double_click)

    # 添加返回按钮
    return_button = tk.Button(result_frame, text="返回", command=return_to_search_from_result, width=20, height=2)
    return_button.pack()

    # 将结果界面的框架隐藏
    result_frame.pack_forget()

    window.mainloop()
