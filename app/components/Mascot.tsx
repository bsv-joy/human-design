import React from 'react';

export function Mascot({ className = "w-12 h-12" }: { className?: string }) {
    return (
        <svg
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={className}
            aria-label="BSV Music Mascot"
        >
            <path
                d="M50 5 L90 25 L90 75 L50 95 L10 75 L10 25 Z"
                stroke="currentColor"
                strokeWidth="2"
                className="text-gold-400"
            />
            <path
                d="M50 20 L80 35 L80 65 L50 80 L20 65 L20 35 Z"
                fill="currentColor"
                className="text-gold-500/20"
            />
            <path
                d="M50 35 L65 42.5 L65 57.5 L50 65 L35 57.5 L35 42.5 Z"
                stroke="currentColor"
                strokeWidth="2"
                className="text-electric-400"
            />
            <circle cx="50" cy="50" r="5" fill="currentColor" className="text-gold-100" />
        </svg>
    );
}
