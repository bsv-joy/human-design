"use client";

import { Play, SkipBack, SkipForward, Volume2 } from "lucide-react";
import { Mascot } from "./Mascot";

export function Player() {
    return (
        <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-white/10 bg-black/80 backdrop-blur-xl">
            <div className="container mx-auto px-6 h-20 flex items-center justify-between">
                <div className="flex items-center gap-4 w-1/3">
                    <div className="w-12 h-12 bg-zinc-900 rounded-sm flex items-center justify-center border border-white/10">
                        <Mascot className="w-6 h-6 text-zinc-600" />
                    </div>
                    <div>
                        <div className="text-sm font-medium text-white">No Track Playing</div>
                        <div className="text-xs text-zinc-500">Select a track to start</div>
                    </div>
                </div>

                <div className="flex flex-col items-center gap-2 w-1/3">
                    <div className="flex items-center gap-6">
                        <button className="text-zinc-400 hover:text-white transition-colors">
                            <SkipBack className="w-5 h-5" />
                        </button>
                        <button className="w-10 h-10 rounded-full bg-white text-black flex items-center justify-center hover:scale-105 transition-transform">
                            <Play className="w-5 h-5 fill-current ml-0.5" />
                        </button>
                        <button className="text-zinc-400 hover:text-white transition-colors">
                            <SkipForward className="w-5 h-5" />
                        </button>
                    </div>
                    <div className="w-full max-w-xs h-1 bg-zinc-800 rounded-full overflow-hidden">
                        <div className="w-0 h-full bg-gold-400" />
                    </div>
                </div>

                <div className="flex items-center justify-end gap-4 w-1/3">
                    <Volume2 className="w-5 h-5 text-zinc-400" />
                    <div className="w-24 h-1 bg-zinc-800 rounded-full overflow-hidden">
                        <div className="w-1/2 h-full bg-zinc-400" />
                    </div>
                </div>
            </div>
        </div>
    );
}
