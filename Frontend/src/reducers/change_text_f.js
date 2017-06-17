const change_text_f = (state = "test", action) => {
  switch (action.type) {
    case 'CHANGE_TEXT':
      return {
        text: action.text
      };
    default:
      return state;
  }
};

export default change_text_f;
