import json
import os


class StudentAI:
    def __init__(self, name, memory_file="memory.json"):
        self.name = name
        self.memory_file = memory_file

        self.concepts = {}
        self.meanings = {}

        # 🧠 apprentissage logique
        self.forbidden_patterns = set()
        self.correct_outputs = {}

        self.load_memory()

    # ---------- MÉMOIRE ----------

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.concepts = data.get("concepts", {})
                self.meanings = data.get("meanings", {})
            print("🧠 Mémoire chargée")
        else:
            print("🧠 Nouvelle mémoire")

    def save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "concepts": self.concepts,
                    "meanings": self.meanings,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
        print("💾 Mémoire sauvegardée")

    # ---------- CONCEPTS ----------

    def learn(self, concept, idea):
        self.concepts.setdefault(concept, 0.5)
        self.meanings.setdefault(concept, [])

        self.concepts[concept] = min(1, self.concepts[concept] + 0.1)

        if idea not in self.meanings[concept]:
            self.meanings[concept].append(idea)

        self.save_memory()

    def explain(self, concept):
        ideas = self.meanings.get(concept, [])
        if not ideas:
            return f"Je ne comprends pas encore ce qu’est {concept}."

        explanation = f"Un(e) {concept} sert à " + " et ".join(ideas)
        if concept == "variable":
            explanation += "\nExemple : x = 5 garde le nombre 5 en mémoire."
        return explanation

    # ---------- RÉPONSE AU CODE ----------

    def answer_code_question(self, code):
        # ✅ si déjà appris → réponse directe
        if code in self.correct_outputs:
            return "Je pense que le programme affiche : " + self.correct_outputs[code]

        guess = self.analyze_code(code)

        if not guess:
            return "Je ne sais pas encore ce que fait ce code."

        # ✅ appliquer règles apprises
        if "Ne pas dupliquer la sortie" in self.forbidden_patterns:
            guess = list(dict.fromkeys(guess))

        return "Je pense que le programme affiche : " + ", ".join(guess)

    # ---------- ANALYSE DU CODE ----------

    def analyze_code(self, code):
        lines = code.split("\n")
        variables = {}
        outputs = []

        execute_block = True
        condition_result = None
        loop_range = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 🔁 FOR LOOP
            if line.startswith("for") and "range" in line:
                var = line.split("for")[1].split("in")[0].strip()
                inside = line[line.find("range(") + 6 : line.find(")")]
                loop_range = list(range(int(inside)))
                continue

            elif "=" in line and not line.startswith(("print", "if", "else")):
                try:
                    name, value = line.split("=")
                    variables[name.strip()] = eval(value.strip(), {}, variables)
                except:
                    pass

            elif line.startswith("print"):
                if loop_range is not None:
                    for v in loop_range:
                        variables[var] = v
                        inside = line[line.find("(") + 1 : line.find(")")]
                        try:
                            outputs.append(str(eval(inside, {}, variables)))
                        except:
                            outputs.append(inside.replace('"', ""))
                    loop_range = None
                else:
                    inside = line[line.find("(") + 1 : line.find(")")]
                    try:
                        outputs.append(str(eval(inside, {}, variables)))
                    except:
                        outputs.append(inside.replace('"', ""))

        return outputs


    # ---------- APPRENTISSAGE LOGIQUE ----------

    def learn_from_logic(self, explanation, code, correct_output):
        # 🔒 mémorisation définitive
        self.correct_outputs[code] = correct_output
        self.forbidden_patterns.add("Ne pas dupliquer la sortie")
