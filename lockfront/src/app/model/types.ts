export type IndexingState = {
    status: string;
    chunks_indexed: number;
}

export type FolderPath = {
    path: string;
}

export type UserQuery = {
    query: string;
}

export type QueryAnswer = {
    answer: string;
    sources: string;
}

export type ChatMsg = {
    id: number;
    time: string;
    role: 'user' | 'assistant';
    text: string;
    sources?: string;
}