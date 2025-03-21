import http from "api/https";
import { @|table_name_pascal|@ } from "constants/@|table_name_pascal|@";

export const create@|table_name_pascal|@ = (data: @|table_name_pascal|@): Promise<any> => {
  return http.post(`/api/v1/@|table_name_pascal|@/Create`, data);
};

export const delete@|table_name_pascal|@ = (id: number): Promise<any> => {
  return http.remove(`/api/v1/@|table_name_pascal|@/Delete?id=${id}`, {});
};

export const get@|table_name_pascal|@ = (id: number): Promise<any> => {
  return http.get(`/api/v1/@|table_name_pascal|@/GetOneById?id=${id}`);
};

export const get@|table_name_plural|@ = (): Promise<any> => {
  return http.get("/api/v1/@|table_name_pascal|@/GetAll");
};

export const update@|table_name_pascal|@ = (data: @|table_name_pascal|@): Promise<any> => {
  return http.put(`/api/v1/@|table_name_pascal|@/Update`, data);
};

@|template_export_mtm_api|@
