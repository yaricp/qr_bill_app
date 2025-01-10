export interface IUserLogin {
    login: string;
    password: string;
}

export interface IUser {
    id: string;
    email: string;
    phone : string;
    login: string;
    tg_name: string;
    tg_id: string;
    password_hash: string;
    lang: string;
}