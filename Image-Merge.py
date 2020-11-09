import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import*
from tkinter import filedialog
from PIL import Image

root = Tk()
root.title("Image Merge")

# 맨 윗줄에 프레임을 먼저 만들어줘야한다.
#파일 프레임(파일 추가, 선택 삭제)
file_frame = Frame(root)
file_frame.pack(fill='x', padx = 5, pady = 5)

#파일 추가 함수
def add_file():
    files = filedialog.askopenfilenames(title = '이미지를 선택하세요', filetypes=(('PNG 파일','*.png'),('모든파일','*.*')), initialdir=r"C:\Users\lemon\Desktop\Visual Studio\Phython\panggame\images") #최초에 C:/ 경로를 보여준다.

    # 사용자가 선택한 파일 목록
    for file in files:
        list_file.insert(END,file)

#선택 삭제 함수
def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

#저장 경로 함수
def browse_save_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '':
        return
    save_path.delete(0,END)
    save_path.insert(0,folder_selected)

#이미지 통합 함수
def merge_image():


    try:
        #가로 넓이
        img_width = cmb_width.get()
        if img_width == '원본유지':
            img_width = -1 #-1일 때는 원본 기준으로 한다.
        else:
            img_width = int(img_width)

        # 간격
        img_space = cmb_space.get()
        if img_space == '좁게':
            img_space = 30
        elif img_space == '보통':
            img_space = 60
        elif img_space == '넓게':
            img_space = 90
        else:# 없음
            img_space = 0

        #포맷
        img_format = cmb_format.get().lower() # PNG, JPG, BMP 값을 받아와서 소문자로 변경

        images = [Image.open(x) for x in list_file.get(0,END)]

        # 이미지 사이즈 리스트에 넣어서 하나씩 처리
        image_sizes = [] # [(width1, height1), (width2, height2), ...]

        if img_width >-1:
            #width변경
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            #원본 사이즈 사용
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        widths, heights = zip(*(image_sizes))

        max_width, total_height = max(widths), sum(heights)

        if img_space >0:#이미지 간격 옵션 적용
            total_height += (img_space* (len(images) -1))


        #스케치북 준비 
        result_img = Image.new('RGB',(max_width,total_height),(255,255,255))
        y_offset = 0 # y 위치 정보

        #이미지 붙여넣기
        for idx, img in enumerate(images):
            #width가 원본이 아닐 때에는 이미지 크기를 조정해야 한다.
            if img_width >-1:
                img = img.resize(image_sizes[idx])
            result_img.paste(img,(0,y_offset))
            y_offset += (img.size[1] + img_space)  #height 값 + 사용자가 지정한 간격

            progress = (idx +1) / len(images) * 100 #실제 percent 정보를 계산
            p_var.set(progress)
            progress_bar.update()

        # 포맷 옵션 처리
        file_name = 'result_photo.' + img_format
        output_path = os.path.join(save_path.get(), file_name)
        result_img.save(output_path)
        msgbox.showinfo('알림','작업이 완료되었습니다.')
    except Exception as err: #예외처리
        msgbox.showinfo('알림',err)


#시작 함수
def start():

    #파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning('경고', '이미지 파일을 추가하세요')
        return

    #저장 경로 확인
    if len(save_path.get()) ==0:
        msgbox.showwarning('경고', '저장 경로를 선택하세요')
        return
    
    merge_image()


# 파일 프레임 안에 파일추가, 선택삭제 버튼을 넣어준다.
btn_add_file = Button(file_frame, padx = 5, pady = 5, width = 12, text ='파일추가', command = add_file)
btn_add_file.pack(side = 'left')

btn_del_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = '선택삭제', command = del_file)
btn_del_file.pack(side = 'right')

#파일 목록들이 들어가는 프레임을 만들어준다.
#리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill = 'both')

#파일이 많을 경우 편리하게 보기 위해 스크롤바가 필요하다.
scrollbar = Scrollbar(list_frame)
scrollbar.pack(side = 'right', fill = 'y')

#리스트 박스를 만들고 스크롤바 작동 명령어를 넣어준다.
list_file = Listbox(list_frame, selectmode = 'extended', height = 15, yscrollcommand = scrollbar.set)
list_file.pack(side = 'left', fill = 'both', expand = True)
scrollbar.config(command = list_file.yview)

#저장 경로를 만들기 위한 레이블 프레임을 만든다.
path_frame = LabelFrame(root, text = '저장경로')
path_frame.pack(fill='x', padx = 5, pady = 5)

#저장 경로
save_path = Entry(path_frame)
save_path.pack(side = 'left', fill = 'x', expand = True, padx = 5, pady = 5)

#찾아보기 버튼 추가
btn_search_file = Button(path_frame, padx = 5, pady = 2, width = 6,text ='찾아보기', command = browse_save_path)
btn_search_file.pack(side = 'right')

#옵션 프레임
option_frame = LabelFrame(root, text = '옵션')
option_frame.pack(fill='x', padx = 5, pady = 5)


#1. 가로 넓이 옵션

#가로 넓이 레이블
lbl_width = Label(option_frame, text = '가로넓이', width =8)
lbl_width.pack(side = 'left')

#가로 넓이 콤보
opt_width = ['원본유지','1024','800','640']
cmb_width = ttk.Combobox(option_frame, state= 'readonly',values = opt_width, width = 10)
cmb_width.current(0)
cmb_width.pack(side = 'left')


#2. 간격 옵션

#간격 옵션 레이블
lbl_space = Label(option_frame, text = '간격', width =8)
lbl_space.pack(side = 'left')

#간격 옵션 콤보
opt_space = ['없음','좁게','보통','넓게']
cmb_space= ttk.Combobox(option_frame, state= 'readonly',values = opt_space, width = 10)
cmb_space.current(0)
cmb_space.pack(side = 'left')


#3. 포멧 옵션

#포멧 옵션 레이블
lbl_format = Label(option_frame, text = '포멧', width =8)
lbl_format.pack(side = 'left')

#포멧 옵션 콤보
opt_format = ['PNG','JPG','BMP']
cmb_format= ttk.Combobox(option_frame, state= 'readonly',values = opt_format, width = 10)
cmb_format.current(0)
cmb_format.pack(side = 'left')

# 진행상황 레이블 프레임을 만든다.
progress_frame = LabelFrame(root, text = '진행상황')
progress_frame.pack(fill='x', padx = 5, pady = 5, ipady = 5)

# 진행상황 프로그래스바
p_var = DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, maximum = 100, variable =p_var)
progress_bar.pack(fill='x', padx = 5, pady = 5)

#실행 프레임 만들기
run_frame = Frame(root)
run_frame.pack(fill='x', padx = 5, pady = 5)

#닫기 버튼
btn_close_file = Button(run_frame, padx = 5, pady = 5, width = 12, text = '닫기', command = root.quit)
btn_close_file.pack(side = 'right')


#시작 버튼
btn_start = Button(run_frame, padx = 5, pady = 5, width = 12, text ='시작', command = start)
btn_start.pack(side = 'right')





root.mainloop()