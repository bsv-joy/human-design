import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

// Basic logging utility
export const logger = {
    logInfo: (message: string, context?: Record<string, any>) => {
        console.log(`[INFO] ${message}`, context || '');
    },
    logError: (message: string, error?: Error, context?: Record<string, any>) => {
        console.error(`[ERROR] ${message}`, error || '', context || '');
    }
};
