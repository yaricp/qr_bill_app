export interface ISeller {
    id: null;
    name: string;
    address: string;
  }

export interface ICountSellerByName {
  name: string;
  count: number;
}

export interface ISummSellerByName {
  name: string;
  summ: number;
}