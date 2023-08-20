# Thời sự
# Thế giới
# Kinh doanh
# bất động sản
# khoa học
# giải trí
# thể thao
# pháp luật
# giao dục
# sức khỏe
# đời sống
# du lịch
# xe cộ
# ----------------------------------------
from ai_communicator import AICommunicator

all_categories = [
    'Thời sự',
    'Thế giới',
    'Kinh doanh',
    'bất động sản',
    'khoa học',
    'giải trí',
    'Ngoại hạng Anh',
    'Bóng đá trong nước',
    'quần vợt',
    'pháp luật',
    'giao dục',
    'sức khỏe',
    'đời sống',
    'du lịch',
    'xe cộ'
]


# Path: ai/ai_communicator.py
# define a method to send an article and ask for classification
def classify(text: str):
    prompt = f"""Câu trả lời dạng json. Hãy phân loại bài báo sau đây vào một trong các loại: {all_categories} trong trường category.
    Đặt tiêu đề cho bài báo trong trường title. Viết lại bài báo đầy đủ thông tin của bài gốc và hấp dẫn hơn trong trường edited_text.
    Tóm tắt bài báo trong trường summary. Trích xuất 3 từ khóa của bài báo trong trường keywords.
    Phân tích cảm xúc của bài báo trong trường sentiment.
    Bài báo cần phân loại, viết lại, tóm tắt, trích xuất từ khóa là: {text}"""
    resp = AICommunicator.compose(prompt, bot_type='edge')
    print(resp)
    return resp['message']


# read articles from file test.txt
def read_articles():
    with open('test.txt', 'r') as f:
        articles = f.readlines()
    return ' '.join(articles)


# test entry point
if __name__ == '__main__':
    text = read_articles()
    answer = classify(text)
    print(answer)
