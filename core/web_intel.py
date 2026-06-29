"""
WEB INTELLIGENCE ENGINE
Real-time internet access for all agents.
Every agent sees live web before answering.
3 search providers — never goes down.
"""
import os, requests
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()

class WebIntel:
    """
    Gives every agent real-time internet access.
    Searches web → extracts content → feeds to agent.
    """

    def __init__(self):
        self.serper_key  = os.getenv("SERPER_API_KEY", "")
        self.tavily_key  = os.getenv("TAVILY_API_KEY", "")
        self.available   = []
        self._check()

    def _check(self):
        if self.serper_key and len(self.serper_key) > 5:
            self.available.append("serper")
            print(f"{Fore.GREEN}✅ Serper (Google) online{Style.RESET_ALL}")
        if self.tavily_key and len(self.tavily_key) > 5:
            self.available.append("tavily")
            print(f"{Fore.GREEN}✅ Tavily (AI Search) online{Style.RESET_ALL}")
        # DuckDuckGo always available — no key needed
        self.available.append("duckduckgo")
        print(f"{Fore.GREEN}✅ DuckDuckGo (backup) online{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🌐 {len(self.available)} search engines ready{Style.RESET_ALL}")

    def search(self, query, max_results=5):
        """
        Search the live web.
        Tries Serper → Tavily → DuckDuckGo
        Returns clean text ready for agents.
        """
        print(f"\n{Fore.YELLOW}🔍 Searching: {query[:50]}...{Style.RESET_ALL}")

        results = None

        if "serper" in self.available:
            results = self._serper(query, max_results)

        if not results and "tavily" in self.available:
            results = self._tavily(query, max_results)

        if not results:
            results = self._duckduckgo(query, max_results)

        if results:
            print(f"{Fore.GREEN}✅ Found {len(results)} results{Style.RESET_ALL}")
            return self._format(query, results)

        return f"No results found for: {query}"

    def _serper(self, query, max_results):
        """Google search via Serper"""
        try:
            r = requests.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": self.serper_key,
                    "Content-Type": "application/json"
                },
                json={
                    "q": query,
                    "num": max_results,
                    "gl": "us",
                    "hl": "en"
                },
                timeout=15
            )
            data = r.json()
            results = []

            # Answer box (if exists)
            if "answerBox" in data:
                ab = data["answerBox"]
                results.append({
                    "title": ab.get("title","Answer"),
                    "snippet": ab.get("answer") or ab.get("snippet",""),
                    "url": ab.get("link",""),
                    "source": "Google Answer Box"
                })

            # Organic results
            for item in data.get("organic", [])[:max_results]:
                results.append({
                    "title": item.get("title",""),
                    "snippet": item.get("snippet",""),
                    "url": item.get("link",""),
                    "source": "Google"
                })

            return results if results else None
        except Exception as e:
            print(f"{Fore.RED}Serper error: {e}{Style.RESET_ALL}")
            return None

    def _tavily(self, query, max_results):
        """AI-optimized search via Tavily"""
        try:
            r = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.tavily_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": max_results,
                    "include_answer": True,
                    "include_raw_content": False
                },
                timeout=15
            )
            data = r.json()
            results = []

            # Direct answer
            if data.get("answer"):
                results.append({
                    "title": "AI Summary",
                    "snippet": data["answer"],
                    "url": "",
                    "source": "Tavily AI"
                })

            # Search results
            for item in data.get("results", [])[:max_results]:
                results.append({
                    "title": item.get("title",""),
                    "snippet": item.get("content",""),
                    "url": item.get("url",""),
                    "source": "Tavily"
                })

            return results if results else None
        except Exception as e:
            print(f"{Fore.RED}Tavily error: {e}{Style.RESET_ALL}")
            return None

    def _duckduckgo(self, query, max_results):
        """DuckDuckGo instant answers — no key needed"""
        try:
            r = requests.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1
                },
                timeout=15
            )
            data = r.json()
            results = []

            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading",""),
                    "snippet": data["AbstractText"],
                    "url": data.get("AbstractURL",""),
                    "source": "DuckDuckGo"
                })

            for topic in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append({
                        "title": topic.get("Text","")[:50],
                        "snippet": topic.get("Text",""),
                        "url": topic.get("FirstURL",""),
                        "source": "DuckDuckGo"
                    })

            return results if results else None
        except Exception as e:
            print(f"{Fore.RED}DuckDuckGo error: {e}{Style.RESET_ALL}")
            return None

    def _format(self, query, results):
        """Format results for agent consumption"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        output = f"🌐 REAL-TIME WEB SEARCH RESULTS\n"
        output += f"Query: {query}\n"
        output += f"Time: {now}\n"
        output += f"{'─'*50}\n\n"

        for i, r in enumerate(results, 1):
            output += f"[{i}] {r['title']}\n"
            output += f"    {r['snippet'][:200]}\n"
            if r.get('url'):
                output += f"    Source: {r['url']}\n"
            output += "\n"

        return output

    def news(self, topic):
        """Get latest news on any topic"""
        return self.search(f"{topic} latest news 2026", max_results=5)

    def research(self, topic):
        """Deep research on any topic"""
        return self.search(f"{topic} comprehensive guide", max_results=8)

    def competitor(self, company):
        """Research competitors"""
        return self.search(
            f"{company} reviews pricing features 2026", max_results=5
        )

    def market(self, industry):
        """Market intelligence"""
        return self.search(
            f"{industry} market trends 2026 statistics", max_results=5
        )

    def price_check(self, service):
        """Check market pricing"""
        return self.search(
            f"{service} pricing cost how much 2026", max_results=5
        )
