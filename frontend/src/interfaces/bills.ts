import { DateTimeFormatResult } from "vue-i18n";
import { ISeller } from "./seller";

export interface IBill {
    id: null;
    created: DateTimeFormatResult;
    value: number;
    image?: string;
    seller: ISeller;
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