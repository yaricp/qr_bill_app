export default interface Tutorial {
    id: null;
    name: string;
    quantity: number;
    unit_price_before_vat: number;
    unit_price_after_vat: number;
    rebate: number;
    rebate_reducing: boolean;
    price_before_vat: number;
    vat_rate: number;
    vat_amount: number;
    price_after_vat: number;
    unit_id: string;
    bill_id: string;
    category_id: string;
  }