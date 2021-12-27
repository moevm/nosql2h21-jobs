import { css } from '@emotion/react';
import styled from '@emotion/styled';

export const VacancyContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;

  border: none;
  border-bottom: 2px solid grey;
  padding: 10px;

  background-color: #fff;

  &:hover {
    background-color: lightgrey;
  }

  ${({ selected }) =>
    selected &&
    css`
      background-color: rgba(92, 201, 245, 0.3);
    `}
`;

export const VacancyTitle = styled.h2`
  color: #443fa2;
  font-size: 16px;
  font-weight: bold;
`;

export const VacancySalary = styled.span`
  color: #909090;
`;

export const VacancyParagraph = styled.p`
  margin-top: 10px;
  color: #909090;
  text-align: left;
`;
