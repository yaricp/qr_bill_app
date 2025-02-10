export interface ISeller {
    id: null;
    name: string;
    official_name: string;
    address: string;
    city: string;
  }

export interface ICountSellerByName {
  name: string;
  count: number;
}

export interface ISummSellerByName {
  name: string;
  summ: number;
}