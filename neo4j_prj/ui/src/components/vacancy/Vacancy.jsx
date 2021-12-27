import { Button } from '@chakra-ui/react';
import { css } from '@emotion/react';

import {
  VacancyContainer,
  VacancyParagraph,
  VacancySalary,
  VacancyTitle,
} from './styles';

export function Vacancy({
  name,
  salaryFrom,
  responsibility,
  Employer: { name: employerName },
  Area: { name: areaName },
  Schedule: { name: scheduleName },
  onClick,
  selected,
  onRemoveClick,
}) {
  return (
    <VacancyContainer onClick={onClick} selected={selected} tabIndex={0}>
      <VacancyTitle>
        {name}
        <VacancySalary>{` от ${salaryFrom}`}</VacancySalary>
      </VacancyTitle>

      <VacancyParagraph>{scheduleName}</VacancyParagraph>
      <VacancyParagraph>{employerName}</VacancyParagraph>
      <VacancyParagraph>{areaName}</VacancyParagraph>
      <VacancyParagraph>{responsibility}</VacancyParagraph>

      <Button
        colorScheme="red"
        css={css`
          align-self: flex-end;
        `}
        onClick={onRemoveClick}
        variant="outline">
        Удалить
      </Button>
    </VacancyContainer>
  );
}
