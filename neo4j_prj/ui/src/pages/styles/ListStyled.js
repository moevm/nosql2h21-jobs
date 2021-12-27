import styled from '@emotion/styled';
import { Link } from '@reach/router';

export const ListStyledContainer = styled.div`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;

  height: auto;
  flex-grow: 1;

  margin: 5vh 5vw 0 5vw;
  background-color: #fff;
  border: 4px solid grey;
`;

export const ListMenu = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;

  width: 20vw;
  height: 100%;
  padding: 20px 10px 20px 20px;
`;

export const ListContent = styled.div`
  position: relative;
  flex-grow: 1;
  padding: 100px 240px 20px 20px;

  height: auto;
`;

export const ListButtonsContainer = styled.div`
  position: fixed;
  top: calc(5vh + 105px);
  right: calc(5vw + 20px);
`;

export const ListButton = styled.button`
  cursor: pointer;
  display: block;
  font-family: inherit;
  font-size: 16px;
  padding: 20px 30px;

  width: 200px;

  border: 2px solid grey;
  background-color: #fff;

  transition: background-color 0.2s ease;

  &:hover {
    background-color: lightgrey;
  }

  & + & {
    margin-top: 20px;
  }
`;

export const ListSearchContainer = styled.div`
  position: absolute;
  top: 20px;
  right: 20px;
  width: calc(100% - 40px);
  display: flex;
`;

export const ListSearchInput = styled.input`
  flex-grow: 1;
  border: 2px solid grey;
  height: 40px;
  font-family: inherit;
  font-size: 16px;
  padding: 0 5px;

  &:focus,
  &:active {
    outline: none;

    border: 2px solid #66615d;
  }
`;

export const ListSearchButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;
  min-width: 40px;
  min-height: 40px;
  padding: 0;
  border: none;

  background-color: #3a39b3;
  color: #fff;
`;

export const ListButtonLink = styled(Link)`
  text-decoration: none;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: inherit;
  padding: 5px 10px;
  margin: 0;
  background-color: rgba(0, 0, 0, 0.00001);
  border: 2px solid #000073;
  color: #fff;
  font-weight: 700;
  background-color: #3235f6;

  width: 180px;
  height: 40px;

  border-radius: 16px;
`;

export const ListItemsContainer = styled.div`
  width: 100%;
  height: auto;
  min-height: 500px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;

  border: 2px solid grey;
`;

export const Filter = styled.div`
  padding: 0 5px;
  margin-top: 20px;
  width: 100%;
  height: auto;

  max-height: 400px;
  overflow-y: auto;
`;

export const FilterTitle = styled.h2`
  font-size: 16px;
  color: #828585;
  margin: 10px 0;
`;

export const FilterValues = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;

  span {
    font-weight: 700;
  }
`;
