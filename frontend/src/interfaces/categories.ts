export interface ICategory {
    id: string;
    name: string;
    user_id: string;
}

export interface ICreateCategory {
    name: string;
}

export interface ICountCategoryByName {
    name: string;
    count: number;
}

export interface ISummCategoryByName {
    name: string;
    summ: number;
}