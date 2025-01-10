export interface IBill {
    id: null;
    created: string;
    summ: number;
}

export interface IBillUrl {
    link: string;
    image: string;
}

export interface ICountBillByName {
    name: string;
    count: number;
}

export interface ISummBillByName {
    name: string;
    summ: number;
}