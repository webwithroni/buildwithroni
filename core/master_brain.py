import os, requests, concurrent.futures
from dotenv import load_dotenv
from colorama import Fore, Style
load_dotenv()

class MasterBrain:

    # ✅ VERIFIED MODEL NAMES FROM LIVE API DOCS
    MODELS = {
        "gemini":   "gemini-2.0-flash",
        "groq":     "llama-3.3-70b-versatile",
        "mistral":  "mistral-large-latest",
        "xai":      "grok-4.3",
        "cerebras": "gpt-oss-120b",
    }

    def __init__(self):
        self.keys = {
            "gemini":   os.getenv("GEMINI_API_KEY",""),
            "groq":     os.getenv("GROQ_API_KEY",""),
            "mistral":  os.getenv("MISTRAL_API_KEY",""),
            "xai":      os.getenv("XAI_API_KEY",""),
            "cerebras": os.getenv("CEREBRAS_API_KEY",""),
        }
        self.available = {}
        self._check()

    def _check(self):
        for name, key in self.keys.items():
            if key and len(key) > 10:
                self.available[name] = True
                print(f"{Fore.GREEN}✅ {name.upper()} ready{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {name.upper()} missing key{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}🧠 {len(self.available)} models online{Style.RESET_ALL}")

    def _gemini(self, prompt):
        # Use v1 (not v1beta) + gemini-2.0-flash
        url = (f"https://generativelanguage.googleapis.com/v1/"
               f"models/{self.MODELS['gemini']}:generateContent"
               f"?key={self.keys['gemini']}")
        try:
            r = requests.post(url, json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": 2048,
                    "temperature": 0.7
                }
            }, timeout=30)
            data = r.json()
            if "error" in data:
                return {"model":"gemini","ok":False,
                        "error":data["error"]["message"]}
            t = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"model":"gemini","text":t,"ok":True}
        except Exception as e:
            return {"model":"gemini","ok":False,"error":str(e)}

    def _groq(self, prompt):
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.keys['groq']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.MODELS["groq"],
                    "messages": [{"role":"user","content":prompt}],
                    "max_tokens": 2048,
                    "temperature": 0.7
                },
                timeout=30)
            data = r.json()
            if "error" in data:
                return {"model":"groq","ok":False,"error":str(data["error"])}
            t = data["choices"][0]["message"]["content"]
            return {"model":"groq","text":t,"ok":True}
        except Exception as e:
            return {"model":"groq","ok":False,"error":str(e)}

    def _mistral(self, prompt):
        try:
            r = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.keys['mistral']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.MODELS["mistral"],
                    "messages": [{"role":"user","content":prompt}],
                    "max_tokens": 2048,
                    "temperature": 0.7
                },
                timeout=30)
            data = r.json()
            if "error" in data:
                return {"model":"mistral","ok":False,"error":str(data["error"])}
            t = data["choices"][0]["message"]["content"]
            return {"model":"mistral","text":t,"ok":True}
        except Exception as e:
            return {"model":"mistral","ok":False,"error":str(e)}

    def _xai(self, prompt):
        # grok-4.3 is current flagship as of June 2026
        try:
            r = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.keys['xai']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.MODELS["xai"],
                    "messages": [{"role":"user","content":prompt}],
                    "max_tokens": 2048,
                    "temperature": 0.7
                },
                timeout=30)
            data = r.json()
            if "error" in data:
                return {"model":"xai","ok":False,"error":str(data["error"])}
            t = data["choices"][0]["message"]["content"]
            return {"model":"xai","text":t,"ok":True}
        except Exception as e:
            return {"model":"xai","ok":False,"error":str(e)}

    def _cerebras(self, prompt):
        # gpt-oss-120b confirmed from your live API response
        try:
            r = requests.post(
                "https://api.cerebras.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.keys['cerebras']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.MODELS["cerebras"],
                    "messages": [{"role":"user","content":prompt}],
                    "max_tokens": 2048,
                    "temperature": 0.7
                },
                timeout=30)
            data = r.json()
            if "error" in data:
                return {"model":"cerebras","ok":False,"error":str(data["error"])}
            t = data["choices"][0]["message"]["content"]
            return {"model":"cerebras","text":t,"ok":True}
        except Exception as e:
            return {"model":"cerebras","ok":False,"error":str(e)}

    def _call(self, model, prompt):
        fn = {
            "gemini":   self._gemini,
            "groq":     self._groq,
            "mistral":  self._mistral,
            "xai":      self._xai,
            "cerebras": self._cerebras,
        }
        return fn[model](prompt) if model in fn else None

    def think(self, prompt, mode="best"):
        if mode == "fast":
            targets = ["cerebras","groq"]
        elif mode == "ensemble":
            targets = list(self.available.keys())
        else:
            targets = list(self.available.keys())[:3]

        targets = [t for t in targets if t in self.available]
        if not targets:
            return "No models available. Check .env keys."

        results = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(targets)
        ) as ex:
            futures = {
                ex.submit(self._call, m, prompt): m
                for m in targets
            }
            for f in concurrent.futures.as_completed(futures):
                r = f.result()
                if r and r.get("ok"):
                    results.append(r)

        if not results:
            return "All models failed. Check internet and keys."

        if mode == "ensemble" and len(results) > 1:
            return self._merge(results, prompt)

        return max(results, key=lambda x: len(x["text"].split()))["text"]

    def _merge(self, results, original):
        combined = "\n\n".join([
            f"[{r['model'].upper()}]:\n{r['text'][:500]}"
            for r in results[:3]
        ])
        merge_prompt = f"""Multiple AI models answered: {original[:150]}

Responses:
{combined}

Create ONE superior merged answer combining the best.
Be comprehensive, specific, well-formatted."""

        for m in ["groq","mistral","cerebras","gemini","xai"]:
            if m in self.available:
                r = self._call(m, merge_prompt)
                if r and r.get("ok"):
                    return r["text"]
        return results[0]["text"]

    def test_all(self):
        print(f"\n{Fore.YELLOW}🧪 Testing all models...{Style.RESET_ALL}")
        print(f"{'─'*40}")
        for model in self.available:
            r = self._call(model, "Reply with exactly one word: ONLINE")
            if r and r.get("ok"):
                preview = r['text'].strip()[:25]
                print(f"{Fore.GREEN}✅ {model.upper():<12} {preview}{Style.RESET_ALL}")
            else:
                err = r.get("error","failed") if r else "no response"
                print(f"{Fore.RED}❌ {model.upper():<12} {err[:40]}{Style.RESET_ALL}")
        print(f"{'─'*40}")

    @property
    def online_count(self):
        return len(self.available)
