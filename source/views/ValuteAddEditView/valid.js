import {
  CheckEmptyLookup,
  CheckEmptyTextField,
  CheckNullOrMore,
  CheckOnlyDigit,
  CheckOnlyText,
  CheckIsEmail,
  CheckIsEqual,
  CheckIsEqualOrGreater,
  CheckIsEqualOrLess,
  CheckIsGreater,
  CheckIsLess,
  CheckMaxLength,
  CheckIdSex,
  CheckMinLength
} from 'src/components/ValidationHelper';



export const validate = (event, validated) => {

 var name = '';
    if (event.target.name === 'name') {
      var nameErrors = [];
      CheckEmptyTextField(event.target.value, nameErrors)
      name = nameErrors.join(', ');
      validated('errorname', name);
    }
    //End of validation field name


 var description = '';
    if (event.target.name === 'description') {
      var descriptionErrors = [];
      description = descriptionErrors.join(', ');
      validated('errordescription', description);
    }
    //End of validation field description


 var code = '';
    if (event.target.name === 'code') {
      var codeErrors = [];
      code = codeErrors.join(', ');
      validated('errorcode', code);
    }
    //End of validation field code


 var queueNumber = '';
    if (event.target.name === 'queueNumber') {
      var queueNumberErrors = [];
      CheckOnlyDigit(event.target.value, queueNumberErrors)
      queueNumber = queueNumberErrors.join(', ');
      validated('errorqueueNumber', queueNumber);
    }
    //End of validation field queueNumber


  
  
  var canSave =
    true
		&& name === ''
		&& description === ''
		&& code === ''
		&& queueNumber === ''
    ;

  return canSave;
}

