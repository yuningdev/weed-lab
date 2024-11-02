import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import tailwindcssAnimate from "tailwindcss-animate";

export function cn(...inputs) {
	return twMerge(clsx(inputs));
}
