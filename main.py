import json
import os

# Quiz Model Class`nclass Quiz:
    """媛쒕퀎 ?댁쫰瑜??쒗쁽?섎뒗 ?대옒??""
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

    def to_dict(self):
        """JSON ??μ쓣 ?꾪빐 媛앹껜瑜??뺤뀛?덈━濡?蹂??""
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer
        }


class QuizGame:
    """?댁쫰 寃뚯엫 ?꾩껜瑜?愿由ы븯???대옒??""
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.file_path = "state.json"
        self.load_data()

    def load_data(self):
        """state.json ?뚯씪?먯꽌 ?곗씠?곕? 遺덈윭?ㅺ굅??湲곕낯 ?곗씠???앹꽦"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.quizzes = [
                        Quiz(q["question"], q["options"], q["answer"])
                        for q in data.get("quizzes", [])
                    ]
            except Exception:
                print("?좑툘 ?곗씠???뚯씪 ?먯긽?쇰줈 湲곕낯 ?곗씠?곕? 濡쒕뱶?⑸땲??")
                self.set_default_quizzes()
        else:
            self.set_default_quizzes()

    def set_default_quizzes(self):
        """湲곕낯 ?댁쫰 5媛??ㅼ젙"""
        default_data = [
            Quiz("?뚯씠??Python)??李쎌떆?먮뒗 ?꾧뎄?쇨퉴??", ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], 1),
            Quiz("由ъ뒪???앹뿉 ?붿냼瑜?異붽??????ъ슜?섎뒗 硫붿꽌?쒕뒗?", ["add()", "append()", "push()", "insert_end()"], 2),
            Quiz("?뚯씠???뚯뒪肄붾뱶 ?뚯씪???뺤옣?먮뒗?", [".py", ".python", ".pyt", ".pyc"], 1),
            Quiz("?뚯씠?ъ뿉???붾㈃??臾몄옣??異쒕젰?????ъ슜?섎뒗 ?⑥닔??", ["console.log()", "printf()", "print()", "System.out.println()"], 3),
            Quiz("李?嫄곗쭞???쒗쁽?섎뒗 ?뚯씠?ъ쓽 ?곗씠????낆??", ["String", "Integer", "Boolean", "Float"], 3)
        ]
        self.quizzes = default_data
        self.save_data()

    def save_data(self):
        """?꾩옱 ?댁쫰 紐⑸줉怨?理쒓퀬 ?먯닔瑜?state.json?????""
        data = {
            "high_score": self.high_score,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes]
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def display_menu(self):
        """硫붿씤 硫붾돱 異쒕젰"""
        print("\n===== Python ?댁쫰 寃뚯엫 =====")
        print("1. ?댁쫰 ?湲?)
        print("2. ?댁쫰 異붽?")
        print("3. ?댁쫰 紐⑸줉 蹂닿린")
        print("4. 理쒓퀬 ?먯닔 蹂닿린")
        print("5. 醫낅즺")

    def run(self):
        """?꾨줈洹몃옩 ?ㅽ뻾 諛?硫붾돱 泥섎━ 猷⑦봽"""
        while True:
            self.display_menu()
            choice = input("?먰븯??硫붾돱 踰덊샇瑜??낅젰?섏꽭?? ").strip()

            if choice == "1":
                print("\n[?댁쫰 ?湲? 湲곕뒫??以鍮?以묒엯?덈떎.")
            elif choice == "2":
                print("\n[?댁쫰 異붽?] 湲곕뒫??以鍮?以묒엯?덈떎.")
            elif choice == "3":
                print("\n[?댁쫰 紐⑸줉 蹂닿린] 湲곕뒫??以鍮?以묒엯?덈떎.")
            elif choice == "4":
                print(f"\n?꾩옱 理쒓퀬 ?먯닔: {self.high_score}??)
            elif choice == "5":
                print("\n?댁쫰 寃뚯엫??醫낅즺?⑸땲?? ?댁슜??二쇱뀛??媛먯궗?⑸땲??")
                break
            else:
                print("\n?좑툘 ?섎せ???낅젰?낅땲?? 1遺??5 ?ъ씠???レ옄瑜??낅젰??二쇱꽭??")


if __name__ == "__main__":
    game = QuizGame()
    game.run()

