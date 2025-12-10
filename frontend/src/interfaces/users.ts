import { ILoginLink } from "@/interfaces/login_link";

export interface IUserLogin {
    login: string;
    password: string;
}

export interface IUser {
    id: string;
    is_admin: boolean;
    email: string;
    email_verified: boolean;
    phone : string;
    login: string;
    tg_name: string;
    tg_verified: boolean;
    tg_id: number;
    password_hash: string;
    lang: string;
    links: ILoginLink[];
}