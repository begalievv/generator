import http from "api/https";
import { @|table_name|@ } from "constants/@|table_name|@";

export const create@|table_name|@ = (data: @|table_name|@): Promise<any> => {
  return http.post(`/@|table_name|@`, data);
};

export const delete@|table_name|@ = (id: number): Promise<any> => {
  return http.remove(`/@|table_name|@/${id}`, {});
};

export const get@|table_name|@ = (id: number): Promise<any> => {
  return http.get(`/@|table_name|@/${id}`);
};

export const get@|table_name_plural|@ = (): Promise<any> => {
  return http.get("/@|table_name|@/GetAll");
};

export const update@|table_name|@ = (data: @|table_name|@): Promise<any> => {
  return http.put(`/@|table_name|@/${data.id}`, data);
};

@|template_export_mtm_api|@
