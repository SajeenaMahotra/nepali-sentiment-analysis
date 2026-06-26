"use client";

import { useState, useEffect, useRef } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

const MODELS = [
  { id: "logistic_regression", label: "Logistic Regression", f1: "0.63", best: true },
  { id: "svm", label: "SVM", f1: "0.60", best: false },
  { id: "naive_bayes", label: "Naive Bayes", f1: "0.51", best: false },
];

const SENTIMENT_CONFIG: Record<string, { label: string; accent: string; bar: string; border: string; glow: string }> = {
  positive: { label: "POSITIVE", accent: "text-emerald-400", bar: "bg-emerald-500", border: "border-emerald-500/30", glow: "shadow-emerald-500/20" },
  negative: { label: "NEGATIVE", accent: "text-rose-400", bar: "bg-rose-500", border: "border-rose-500/30", glow: "shadow-rose-500/20" },
  neutral: { label: "NEUTRAL", accent: "text-amber-400", bar: "bg-amber-400", border: "border-amber-400/30", glow: "shadow-amber-400/20" },
};

const BAR_COLORS: Record<string, string> = {
  positive: "bg-emerald-500",
  negative: "bg-rose-500",
  neutral: "bg-amber-400",
};

const EXAMPLES = [
  "ekdam ramro product ho, delivery pani fast thiyo",
  "worst product ever, complete waste of money",
  "packaging thikai thiyo, product average lagyo",
];

function AnimatedBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles: { x: number; y: number; vx: number; vy: number; size: number; alpha: number }[] = [];
    const count = 60;

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        size: Math.random() * 1.5 + 0.5,
        alpha: Math.random() * 0.4 + 0.1,
      });
    }

    let animId: number;

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(99, 102, 241, ${0.15 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }

      // Draw particles
      particles.forEach((p) => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(139, 92, 246, ${p.alpha})`;
        ctx.fill();

        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
      });

      animId = requestAnimationFrame(draw);
    };

    draw();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none z-0" />;
}

export default function Home() {
  const [text, setText] = useState("");
  const [model, setModel] = useState("logistic_regression");
  const [result, setResult] = useState<null | {
    sentiment: string;
    probabilities: Record<string, number>;
    cleaned_text: string;
  }>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 60000); // 60 second timeout
      const res = await fetch("https://nepali-sentiment-analysis-1.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, model }),
        signal: controller.signal,
      });
      clearTimeout(timeout);
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (e: unknown) {
      if (e instanceof Error && e.name === 'AbortError') {
        setError("Server is waking up — please try again in a moment.");
      } else {
        setError(e instanceof Error ? e.message : "Something went wrong");
      }
    };

    const config = result ? SENTIMENT_CONFIG[result.sentiment] : null;

    return (
      <main className="min-h-screen bg-[#0a0a0f] text-white relative overflow-hidden">
        <AnimatedBackground />

        {/* Gradient orbs */}
        <div className="fixed top-[-20%] left-[-10%] w-[500px] h-[500px] bg-violet-900/20 rounded-full blur-[120px] pointer-events-none z-0" />
        <div className="fixed bottom-[-20%] right-[-10%] w-[500px] h-[500px] bg-indigo-900/20 rounded-full blur-[120px] pointer-events-none z-0" />

        <div className="relative z-10 flex min-h-screen">

          {/* Sidebar */}
          <div className="hidden lg:flex flex-col justify-between w-64 min-h-screen border-r border-white/5 px-6 py-10 bg-white/[0.02] backdrop-blur-sm shrink-0">
            <div className="space-y-8">
              <div>
                <div className="flex items-end gap-[4px] mb-5">
                  <div className="w-[6px] h-[12px] bg-violet-500 rounded-sm opacity-60" />
                  <div className="w-[6px] h-[20px] bg-violet-500 rounded-sm" />
                  <div className="w-[6px] h-[15px] bg-violet-500 rounded-sm opacity-80" />
                </div>
                <p className="text-[10px] uppercase tracking-widest text-white/30 font-medium mb-1">Tool</p>
                <p className="text-sm font-semibold text-white/80">Sentiment Analyzer</p>
              </div>

              <div className="space-y-1">
                <p className="text-[10px] uppercase tracking-widest text-white/30 font-medium mb-3">Models</p>
                {MODELS.map((m) => (
                  <button
                    key={m.id}
                    onClick={() => { setModel(m.id); setResult(null); }}
                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm transition-all ${model === m.id
                      ? "bg-white/10 text-white border border-white/10"
                      : "text-white/40 hover:bg-white/5 hover:text-white/70"
                      }`}
                  >
                    <span className="font-medium truncate">{m.label}</span>
                    <span className="flex items-center gap-1.5 ml-2 shrink-0">
                      <span className={`text-xs font-mono ${model === m.id ? "text-white/50" : "text-white/20"}`}>{m.f1}</span>
                      {m.best && (
                        <span className="bg-emerald-500 text-white text-[9px] px-1.5 py-0.5 rounded-full font-bold">
                          BEST
                        </span>
                      )}
                    </span>
                  </button>
                ))}
              </div>

              <div>
                <p className="text-[10px] uppercase tracking-widest text-white/30 font-medium mb-3">About</p>
                <p className="text-xs text-white/30 leading-relaxed">
                  Classifies sentiment in code-mixed Romanized Nepali-English reviews from Daraz Nepal.
                </p>
                <p className="text-xs text-white/15 leading-relaxed mt-2">
                  TF-IDF · Bigrams · Macro F1 · 4,343 reviews
                </p>
              </div>
            </div>
            <p className="text-[10px] text-white/15">Daraz Nepal · Nepali-English NLP</p>
          </div>

          {/* Main */}
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="w-full max-w-lg space-y-7">

              <div className="space-y-1.5">
                <h1 className="text-4xl font-semibold tracking-tight text-white">
                  Analyze a Review
                </h1>
                <p className="text-white/40 text-sm">
                  Paste a product review to classify its sentiment.
                </p>
              </div>

              {/* Mobile models */}
              <div className="flex gap-2 flex-wrap lg:hidden">
                {MODELS.map((m) => (
                  <button
                    key={m.id}
                    onClick={() => { setModel(m.id); setResult(null); }}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${model === m.id
                      ? "bg-white/10 text-white border-white/20"
                      : "text-white/40 border-white/10 hover:border-white/20 hover:text-white/70"
                      }`}
                  >
                    {m.label} <span className="opacity-50">F1 {m.f1}</span>
                  </button>
                ))}
              </div>

              {/* Textarea */}
              <div className="space-y-2.5">
                <Textarea
                  placeholder="ekdam ramro product ho, delivery pani fast thiyo..."
                  className="min-h-[130px] resize-none bg-white/5 border-white/10 text-white placeholder:text-white/20 focus:border-violet-500/50 text-sm rounded-xl backdrop-blur-sm transition-all"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
                <div className="flex flex-wrap gap-1.5">
                  {EXAMPLES.map((ex) => (
                    <button
                      key={ex}
                      onClick={() => setText(ex)}
                      className="text-[11px] text-white/30 hover:text-white/60 border border-white/10 hover:border-white/20 px-3 py-1 rounded-full transition-all"
                    >
                      {ex.length > 36 ? ex.slice(0, 36) + "…" : ex}
                    </button>
                  ))}
                </div>
              </div>

              <Button
                onClick={handleSubmit}
                disabled={loading || !text.trim()}
                className="w-full h-11 bg-violet-600 hover:bg-violet-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-violet-500/25 transition-all disabled:opacity-30"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Analyzing...
                  </span>
                ) : "Analyze Sentiment"}
              </Button>

              {error && (
                <div className="text-rose-400 text-sm border border-rose-500/20 bg-rose-500/10 rounded-xl px-4 py-3">
                  {error}
                </div>
              )}

              {result && config && (
                <div className={`bg-white/5 backdrop-blur-sm border ${config.border} rounded-xl p-6 space-y-5 shadow-xl ${config.glow}`}>
                  <div className="flex items-center justify-between">
                    <p className="text-[10px] uppercase tracking-widest text-white/30 font-medium">Result</p>
                  </div>

                  <p className={`text-5xl font-bold tracking-tight ${config.accent}`}>
                    {config.label}
                  </p>

                  <div className="space-y-3">
                    {Object.entries(result.probabilities)
                      .sort((a, b) => b[1] - a[1])
                      .map(([label, prob]) => {
                        const isScore = prob < 0;
                        const displayVal = isScore ? prob.toFixed(3) : `${(prob * 100).toFixed(1)}%`;
                        const barWidth = isScore ? Math.min(Math.abs(prob) * 30, 100) : prob * 100;
                        return (
                          <div key={label} className="space-y-1.5">
                            <div className="flex justify-between text-xs">
                              <span className="capitalize text-white/50">{label}</span>
                              <span className="text-white/40 font-mono">{displayVal}</span>
                            </div>
                            <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                              <div
                                className={`h-full ${BAR_COLORS[label] ?? "bg-white/30"} rounded-full transition-all duration-700`}
                                style={{ width: `${barWidth}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}
                  </div>

                  <div className="text-xs text-white/30 font-mono bg-white/5 rounded-lg px-3 py-2 border border-white/5">
                    <span className="text-white/40 font-sans font-medium">Preprocessed: </span>
                    {result.cleaned_text || <span className="italic">empty after cleaning</span>}
                  </div>
                </div>
              )}

            </div>
          </div>
        </div>
      </main>
    );
  }