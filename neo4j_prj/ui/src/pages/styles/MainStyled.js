import styled from '@emotion/styled';
import { Link } from '@reach/router';

export const MainContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;

  height: 100%;
  width: 100%;

  padding: 10vh;
`;

export const ExportImportButtonsContainer = styled.div`
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: flex-end;
`;

export const ExportImportButton = styled.button`
  cursor: pointer;
  font-family: inherit;
  padding: 5px 10px;
  margin: 0;
  background-color: rgba(0, 0, 0, 0.00001);
  border: 2px solid #fff;
  color: #fff;
  font-weight: 700;

  backdrop-filter: blur(10px);

  border-radius: 16px;

  & + & {
    margin-left: 2vw;
  }
`;

export const MainContent = styled.div`
  width: 100%;
`;

export const MainHeader = styled.h1`
  padding: 0;
  color: #fff;

  font-size: 42px;
`;

export const MainSearchContainer = styled.div`
  margin-top: 40px;
  width: 100%;
  display: flex;
`;

export const MainSearchInput = styled.input`
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

export const MainSearchButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;
  min-width: 40px;
  min-height: 40px;
  padding: 0;
  border: none;

  background-color: #37797f;
  color: #fff;
`;

export const MainLink = styled(Link)`
  display: block;
  color: #fff;
  font-size: 18px;
  margin-top: 10px;
`;

export const VacancyList = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

export const VacancyItemHeader = styled.h2`
  color: #355f64;
  font-weight: 700;
  overflow-wrap: break-word;
`;

export const VacancyItemParagraph = styled.p`
  margin-top: 20px;
  color: #646663;
  font-weight: 700;

  & + & {
    margin-top: 5px;
  }
`;

export const VacancyItem = styled.div`
  background-color: #fff;
  padding: 20px 5px;
  border-radius: 20px;
  border: 2px solid grey;

  height: 180px;
  width: 30%;

  display: flex;
  flex-direction: column;
  justify-content: flex-start;

  &:nth-of-type(2) {
    ${VacancyItemHeader} {
      color: #d47a4e;
    }
  }

  &:nth-of-type(3) {
    ${VacancyItemHeader} {
      color: #e29951;
    }
  }
`;
