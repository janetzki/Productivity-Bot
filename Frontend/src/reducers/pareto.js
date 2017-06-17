

const pareto = (state = {}, action) => {
    switch (action.type) {
        case 'LOAD_PARETO':
            return {
                    pareto_data: action.file
            };
        default:
            return state;
        
  }
};

export default pareto;