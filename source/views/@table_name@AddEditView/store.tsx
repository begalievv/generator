import { makeAutoObservable, runInAction } from "mobx";
import i18n from "i18next";
import dayjs from "dayjs";
import MainStore from "MainStore";
import { validate, validateField } from "./valid";
import { get@|table_name|@ } from "api/@|table_name|@";
import { create@|table_name|@ } from "api/@|table_name|@";
import { update@|table_name|@ } from "api/@|table_name|@";

 // dictionaries
@|template_store_import_dictionaries|@

class NewStore {
  @|template_store_init|@

  errors: { [key: string]: string } = {};

  // Справочники
  @|template_store_init_dictionaries|@


  constructor() {
    makeAutoObservable(this);
  }

  clearStore() {
    runInAction(() => {
      @|template_store_clear|@
      this.errors = {}
    });
  }

  handleChange(event) {
    const { name, value } = event.target;
    (this as any)[name] = value;
    this.validateField(name, value);
  }

  async validateField(name: string, value: any) {
    const { isValid, error } = await validateField(name, value);
    if (isValid) {
      this.errors[name] = ""; 
    } else {
      this.errors[name] = error;
    }
  }

  async onSaveClick(onSaved: (id: number) => void) {
    var data = {
      @|template_store_validate|@
    };

    const { isValid, errors } = await validate(data);
    if (!isValid) {
      this.errors = errors;
      MainStore.openErrorDialog(i18n.t("message:error.alertMessageAlert"));
      return;
    }

    try {
      MainStore.changeLoader(true);
      let response;
      if (this.id === 0) {
        response = await create@|table_name|@(data);
      } else {
        response = await update@|table_name|@(data);
      }
      if (response.status === 201 || response.status === 200) {
        onSaved(response);
        if (data.id === 0) {
          MainStore.setSnackbar(i18n.t("message:snackbar.successSave"), "success");
        } else {
          MainStore.setSnackbar(i18n.t("message:snackbar.successEdit"), "success");
        }
      } else {
        throw new Error();
      }
    } catch (err) {
      MainStore.setSnackbar(i18n.t("message:somethingWentWrong"), "error");
    } finally {
      MainStore.changeLoader(false);
    }
  };

  async doLoad(id: number) {

    //загрузка справочников
    @|template_store_doload_dict|@

    if (id === null || id === 0) {
      return;
    }
    this.id = id;

    this.load@|table_name|@(id);
  }

  load@|table_name|@ = async (id: number) => {
    try {
      MainStore.changeLoader(true);
      const response = await get@|table_name|@(id);
      if ((response.status === 201 || response.status === 200) && response?.data !== null) {
        runInAction(() => {
          @|template_store_set_data|@
        });
      } else {
        throw new Error();
      }
    } catch (err) {
      MainStore.setSnackbar(i18n.t("message:somethingWentWrong"), "error");
    } finally {
      MainStore.changeLoader(false);
    }
  };

  @|template_store_load_dictionaries|@

}

export default new NewStore();
