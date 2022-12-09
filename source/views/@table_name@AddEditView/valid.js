import {
  CheckEmptyLookup,
  CheckEmptyTextField,
  CheckNullOrMore,
  CheckOnlyDigit,
  CheckCorrectDate,
  CheckCorrectDateNullable,
} from 'src/components/ValidationHelper';


export const validate = (event, validated) => {

  @|template_valid_fields|@



  var canSave =
    true
    @|template_valid_check_cansave|@
    ;

  return canSave;
}

