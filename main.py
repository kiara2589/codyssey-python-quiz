import json
import os
import shutil

class Quiz:
    """개별 퀴즈 모델 클래스 (문제, 선택지, 정답 관리)"""
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
    """퀴즈 게임 데이터 관리, 게임 진행, 데이터 IO 제어 클래스"""
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.file_path = "state.json"
        self.backup_path = "state.json.bak"
        self.load_data()

    def load_data(self):
        """state.json 파일에서 데이터를 불러오고 구체적 예외 대응"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.quizzes = [
                        Quiz(q["question"], q["options"], q["answer"])
                        for q in data.get("quizzes", [])
                    ]
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ 데이터 파일 손상 또는 읽기 오류 ({type(e).__name__}). 백업 복구 또는 기본 데이터를 로드합니다.")
                self.restore_backup_or_default()
            except Exception as e:
                print(f"⚠️ 알 수 없는 오류 발생: {e}. 기본 데이터를 로드합니다.")
                self.set_default_quizzes()
        else:
            self.set_default_quizzes()

    def restore_backup_or_default(self):
        """백업 파일이 존재할 경우 복구, 실패 시 기본 데이터 설정"""
        if os.path.exists(self.backup_path):
            try:
                shutil.copy(self.backup_path, self.file_path)
                print("🔄 백업 파일(state.json.bak)로부터 성공적으로 복구되었습니다.")
                self.load_data()
                return
            except Exception:
                pass
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
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장 및 백업 생성"""
        data = {
            "high_score": self.high_score,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes]
        }
        # 백업 생성
        if os.path.exists(self.file_path):
            try:
                shutil.copy(self.file_path, self.backup_path)
            except Exception:
                pass

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

    def play_quiz(self):
        """퀴즈 풀기 및 정답 검증/점수 갱신"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n🎮 퀴즈를 시작합니다! (총 {len(self.quizzes)}문항)")
        score = 0

        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {idx}] {quiz.question}")
            for opt_idx, option in enumerate(quiz.options, start=1):
                print(f"  {opt_idx}. {option}")
            
            user_input = input("정답 번호 입력 (1-4): ").strip()
            if user_input.isdigit() and int(user_input) == quiz.answer:
                print("⭕ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다! (정답: {quiz.answer}번)")

        print(f"\n🏆 게임 종료! 최종 점수: {score} / {len(self.quizzes)}")
        if score > self.high_score:
            print(f"🎉 축하합니다! 새로운 최고 점수 달성! ({self.high_score}점 ➔ {score}점)")
            self.high_score = score
            self.save_data()

    def add_quiz(self):
        """퀴즈 추가 및 유효성 검증, 데이터 저장"""
        print("\n➕ 새로운 퀴즈 추가")
        question = input("문제 내용: ").strip()
        if not question:
            print("❌ 잘못된 입력입니다. 문제 내용은 비워둘 수 없습니다.")
            return

        options = []
        for i in range(1, 5):
            opt = input(f"선택지 {i}: ").strip()
            if not opt:
                print("❌ 잘못된 입력입니다. 선택지는 비워둘 수 없습니다.")
                return
            options.append(opt)

        ans_input = input("정답 번호 (1-4): ").strip()
        if not ans_input.isdigit() or int(ans_input) not in [1, 2, 3, 4]:
            print("❌ 잘못된 입력입니다. 정답 번호는 1~4 사이의 숫자여야 합니다.")
            return

        new_quiz = Quiz(question, options, int(ans_input))
        self.quizzes.append(new_quiz)
        self.save_data()
        print("✅ 새 퀴즈가 성공적으로 추가 및 저장되었습니다!")

    def show_quizzes(self):
        """퀴즈 목록 보기"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📜 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{idx}] {quiz.question}")
            for opt_idx, option in enumerate(quiz.options, start=1):
                print(f"    {opt_idx}) {option}")
            print(f"    👉 정답: {quiz.answer}번")

    def run(self):
        """프로그램 실행 메인 루프 (KeyboardInterrupt, EOFError 대응)"""
        while True:
            try:
                self.display_menu()
                choice = input("원하는 메뉴 번호를 입력하세요: ").strip()

                if choice == "1":
                    self.play_quiz()
                elif choice == "2":
                    self.add_quiz()
                elif choice == "3":
                    self.show_quizzes()
                elif choice == "4":
                    print(f"\n현재 최고 점수: {self.high_score}점")
                elif choice == "5":
                    print("\n퀴즈 게임을 종료합니다. 이용해 주셔서 감사합니다!")
                    break
                else:
                    print("\n❌ 잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 사용자에 의해 강제 종료되었습니다. 안전하게 프로그램을 종료합니다.")
                break


if __name__ == "__main__":
    game = QuizGame()
    game.run()