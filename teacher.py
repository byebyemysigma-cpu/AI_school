class TeacherAI:
    def __init__(self, name="Prof"):
        self.name = name
        
    def explain_if_else(self, code, correct_output):
        explanation = (
            "Une condition if est évaluée comme vraie ou fausse.\n"
            "Si la condition est vraie, le bloc if s’exécute.\n"
            "Sinon, le bloc else s’exécute.\n"
            f"Ici, le programme affiche : {correct_output}"
        )
        return explanation
    
    def teach_from_error(self, student, code):
        print("\n🧪 Tentative de l'élève")
        predicted = student.answer_code_question(code)
        print("🤖 Élève :", predicted)

        correct = ", ".join(self.execute_code(code))
        print("👨‍🏫 Prof : Résultat réel :", correct)

        if predicted.replace("Je pense que le programme affiche : ", "") == correct:
            print("✅ Prof : Bonne réponse du premier coup.")
            return

        print("❌ Prof : Ce n’est pas correct.")

        explanation = self.explain_correction(code, predicted, correct)
        print("📘 Explication du prof")
        print(explanation)

        # 🧠 APPRENTISSAGE (IMPORTANT)
        student.learn_from_explanation(explanation)

        print("\n🔁 Nouvelle tentative de l'élève")
        improved = student.answer_code_question(code)
        print("🤖 Élève :", improved)

    def execute_code(self, code):
        outputs = []

        try:
            exec(
                code,
                {},
                {
                    "print": lambda x: outputs.append(str(x))
                }
            )
        except Exception as e:
            outputs.append("Erreur")

        return outputs

    def explain_correction(self, code, predicted, correct):
        return {
        "explanation": (
            "Une condition if est évaluée comme vraie ou fausse. "
            "Si la condition est vraie, le bloc if s'exécute. "
            "Sinon, le bloc else s'exécute. "
            "Ici, la condition est fausse, donc le programme affiche 'petit'."
        ),
        "correct_output": ["petit"],
        "error": "Tu as répété la sortie deux fois",
        "rule": "Ne pas dupliquer la sortie"
    }
    


