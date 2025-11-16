// type.ts
export type Question = {
  id: string;
  type?: "text" | "textarea" | "slider";
  label?: string;
  placeholder?: string;
  default?: string | number;
  scale_min?: number;
  scale_max?: number;
  text?: string;
};

export type QA = Record<string, string | number | boolean | null | undefined>;

export type Message = {
  role: "user" | "assistant";
  content: string;
};
