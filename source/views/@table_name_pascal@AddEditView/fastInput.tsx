import React, { FC, useEffect } from "react";
import { Card, CardContent, Divider, Paper, Grid, Container, IconButton, Box } from "@mui/material";
import { useTranslation } from "react-i18next";
import store from "./store";
import { observer } from "mobx-react";
import LookUp from "components/LookUp";
import CustomTextField from "components/TextField";
import CustomCheckbox from "components/Checkbox";
import DateTimeField from "components/DateTimeField";
import storeList from "./../@|table_name_pascal|@ListView/store";
import CreateIcon from "@mui/icons-material/Create";
import DeleteIcon from "@mui/icons-material/Delete";
import CustomButton from "components/Button";

type @|table_name_pascal|@Props = {
  children?: React.ReactNode;
  isPopup?: boolean;
  mainId: number;
};

const FastInputView: FC<@|table_name_pascal|@Props> = observer((props) => {
  const { t } = useTranslation();
  const translate = t;

  useEffect(() => {
    if (props.mainId !== 0 && storeList.mainId !== props.mainId) {
      storeList.mainId = props.mainId;
      storeList.load@|table_name_plural|@();
    }
  }, [props.mainId]);

  const columns = [
    @|template_fast_input_columns|@
  ];

  return (
    <Container>
      <Card component={Paper} elevation={5}>
        <CardContent>
          <Box id="@|table_name_pascal|@_TitleName" sx={{ m: 1 }}>
            <h3>{translate("label:@|table_name_pascal|@AddEditView.entityTitle")}</h3>
          </Box>
          <Divider />
          <Grid container direction="row" justifyContent="center" alignItems="center" spacing={1}>
            {columns.map((col) => {
              const id = "id_c_title_EmployeeContact_" + col.field;
              if (col.width == null) {
                return (
                  <Grid id={id} item xs sx={{ m: 1 }}>
                    <strong> {col.headerName}</strong>
                  </Grid>
                );
              } else
                return (
                  <Grid id={id} item xs={null} sx={{ m: 1 }}>
                    <strong> {col.headerName}</strong>
                  </Grid>
                );
            })}
            <Grid item xs={1}></Grid>
          </Grid>
          <Divider />

          {storeList.data.map((entity) => {
            const style = { backgroundColor: entity.id === store.id && "#F0F0F0" };
            return (
              <>
                <Grid
                  container
                  direction="row"
                  justifyContent="center"
                  alignItems="center"
                  sx={style}
                  spacing={1}
                  id="id_EmployeeContact_row"
                >
                  {columns.map((col) => {
                    const id = "id_EmployeeContact_" + col.field + "_value";
                    if (col.width == null) {
                      return (
                        <Grid item xs id={id} sx={{ m: 1 }}>
                          {entity[col.field]}
                        </Grid>
                      );
                    } else
                      return (
                        <Grid item xs={col.width} id={id} sx={{ m: 1 }}>
                          {entity[col.field]}
                        </Grid>
                      );
                  })}
                  <Grid item display={"flex"} justifyContent={"center"} xs={1}>
                    {storeList.isEdit === false && (
                      <>
                        <IconButton
                          id="id_EmployeeContactEditButton"
                          name="edit_button"
                          style={{ margin: 0, marginRight: 5, padding: 0 }}
                          onClick={() => {
                            storeList.setFastInputIsEdit(true);
                            store.doLoad(entity.id);
                          }}
                        >
                          <CreateIcon />
                        </IconButton>
                        <IconButton
                          id="id_EmployeeContactDeleteButton"
                          name="delete_button"
                          style={{ margin: 0, padding: 0 }}
                          onClick={() => storeList.delete@|table_name_pascal|@(entity.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </>
                    )}
                  </Grid>
                </Grid>
                <Divider />
              </>
            );
          })}

          {storeList.isEdit ? (
            <Grid container spacing={3} sx={{ mt: 2 }}>
              @|template_base_fields|@
              <Grid item xs={12} display={"flex"} justifyContent={"flex-end"}>
                <CustomButton
                  variant="contained"
                  size="small"
                  id="id_@|table_name_pascal|@SaveButton"
                  sx={{ mr: 1 }}
                  onClick={() => {
                    store.onSaveClick((id: number) => {
                      storeList.setFastInputIsEdit(false);
                      storeList.load@|table_name_plural|@();
                      store.clearStore();
                    });
                  }}
                >
                  {translate("common:save")}
                </CustomButton>
                <CustomButton
                  variant="contained"
                  size="small"
                  id="id_@|table_name_pascal|@CancelButton"
                  onClick={() => {
                    storeList.setFastInputIsEdit(false);
                    store.clearStore();
                  }}
                >
                  {translate("common:cancel")}
                </CustomButton>
              </Grid>
            </Grid>
          ) : (
            <Grid item display={"flex"} justifyContent={"flex-end"} sx={{ mt: 2 }}>
              <CustomButton
                variant="contained"
                size="small"
                id="id_@|table_name_pascal|@AddButton"
                onClick={() => {
                  storeList.setFastInputIsEdit(true);
                  store.doLoad(0);
                  // store.project_id = props.mainId;
                }}
              >
                {translate("common:add")}
              </CustomButton>
            </Grid>
          )}
        </CardContent>
      </Card>
    </Container>
  );
});

export default FastInputView;
