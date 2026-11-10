import json
import os

class Quiz:
    """개별 퀴즈를 표현하는 클래스"""
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

    def to_dict(self):
        """JSON 저장을 위해 객체를 딕셔너리로 변환"""
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer
        }


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.file_path = "state.json"
        self.load_data()

    def load_data(self):
        """state.json 파일에서 데이터를 불러오거나 기본 데이터 생성"""
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
                print("⚠️ 데이터 파일 손상으로 기본 데이터를 로드합니다.")
                self.set_default_quizzes()
        else:
            self.set_default_quizzes()

    def set_default_quizzes(self):
        """기본 퀴즈 5개 설정"""
        default_data = [
            Quiz("파이썬(Python)의 창시자는 누구일까요?", ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], 1),
            Quiz("리스트 끝에 요소를 추가할 때 사용하는 메서드는?", ["add()", "append()", "push()", "insert_end()"], 2),
            Quiz("파이썬 소스코드 파일의 확장자는?", [".py", ".python", ".pyt", ".pyc"], 1),
            Quiz("파이썬에서 화면에 문장을 출력할 때 사용하는 함수는?", ["console.log()", "printf()", "print()", "System.out.println()"], 3),
            Quiz("참/거짓을 표현하는 파이썬의 데이터 타입은?", ["String", "Integer", "Boolean", "Float"], 3)
        ]
        self.quizzes = default_data
        self.save_data()

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장"""
        data = {
            "high_score": self.high_score,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes]
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def display_menu(self):
        """메인 메뉴 출력"""
        print("\n===== Python 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 보기")
        print("5. 종료")

    def run(self):
        """프로그램 실행 및 메뉴 처리 루프"""
        while True:
            self.display_menu()
            choice = input("원하는 메뉴 번호를 입력하세요: ").strip()

            if choice == "1":
                print("\n[퀴즈 풀기] 기능을 준비 중입니다.")
            elif choice == "2":
                print("\n[퀴즈 추가] 기능을 준비 중입니다.")
            elif choice == "3":
                print("\n[퀴즈 목록 보기] 기능을 준비 중입니다.")
            elif choice == "4":
                print(f"\n현재 최고 점수: {self.high_score}점")
            elif choice == "5":
                print("\n퀴즈 게임을 종료합니다. 이용해 주셔서 감사합니다!")
                break
            else:
                print("\n⚠️ 잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해 주세요.")


if __name__ == "__main__":
    game = QuizGame()
    game.run()