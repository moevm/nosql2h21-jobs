import { HiSearchCircle } from 'react-icons/all';

import { Modal, useModal } from '../components';
import {
  ExportImportButton,
  ExportImportButtonsContainer,
  MainContainer,
  MainContent,
  MainHeader,
  MainLink,
  MainSearchButton,
  MainSearchContainer,
  MainSearchInput,
  VacancyItem,
  VacancyItemHeader,
  VacancyItemParagraph,
  VacancyList,
} from './styles';

const vacancies = [
  {
    name: 'Востребованные вакансии',
    key: 'top_need',
  },
  {
    name: 'Высокооплачиваемые вакансии',
    key: 'top_paid',
  },
  {
    name: 'Новые вакансии',
    key: 'top_new',
  },
];

export function Main() {
  const {
    isModalOpened: isExportOpen,
    handleModalOpen: handleOpenExport,
    handleModalClose: handleExportClose,
  } = useModal();

  const {
    isModalOpened: isImportOpen,
    handleModalOpen: handleOpenImport,
    handleModalClose: handleImportClose,
  } = useModal();

  return (
    <MainContainer>
      <ExportImportButtonsContainer>
        <ExportImportButton onClick={handleOpenExport}>
          экспорт БД
        </ExportImportButton>

        <ExportImportButton onClick={handleOpenImport}>
          импорт БД
        </ExportImportButton>
      </ExportImportButtonsContainer>

      <MainContent>
        <MainHeader>Поиск вакансий</MainHeader>
        <MainSearchContainer>
          <MainSearchInput placeholder="Профессия, должность или вакансия" />

          <MainSearchButton>
            <HiSearchCircle size={35} />
          </MainSearchButton>
        </MainSearchContainer>

        <MainLink to="/">посмотреть список</MainLink>
      </MainContent>

      <VacancyList>
        {vacancies.map(({ name, key }) => (
          <VacancyItem key={key}>
            <VacancyItemHeader>{name}</VacancyItemHeader>

            <VacancyItemParagraph>35000-85000 руб.</VacancyItemParagraph>
            <VacancyItemParagraph>14 вакансий</VacancyItemParagraph>
          </VacancyItem>
        ))}
      </VacancyList>

      <Modal onClose={handleExportClose} open={isExportOpen}>
        <div>KEK</div>
      </Modal>

      <Modal onClose={handleImportClose} open={isImportOpen}>
        <div>LOL</div>
      </Modal>
    </MainContainer>
  );
}
