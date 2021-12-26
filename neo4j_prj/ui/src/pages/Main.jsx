import { useCallback, useEffect, useState } from 'react';
import { FcDownload, FcUpload, HiSearchCircle } from 'react-icons/all';

import { Modal, useModal } from '../components';
import { plural } from '../utils/plural';
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
  ModalButton,
  Vacancy,
  VacancyItem,
  VacancyItemHeader,
  VacancyItemParagraph,
  VacancyList,
  VacancyNote,
  VacancyNoteContainer,
  VacancyTitle,
} from './styles';

const vacancies = [
  {
    name: 'Востребованные вакансии',
    key: 'top_need',
    url: 'http://94.26.231.106:5000/api/vacancy/top_need/0/4',
  },
  {
    name: 'Высокооплачиваемые вакансии',
    key: 'top_paid',
    url: 'http://94.26.231.106:5000/api/vacancy/top_paid/0/4',
  },
  {
    name: 'Новые вакансии',
    key: 'top_new',
    url: 'http://94.26.231.106:5000/api/vacancy/top_new/0/4',
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

  const [data, setData] = useState([]);

  const [vacancyId, setVacancyId] = useState(-1);
  const [vacancyNoteShown, setVacancyNoteShown] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      const sourcesRequests = vacancies.map(({ url }) => fetch(url));

      const sourcesResponses = await Promise.all(sourcesRequests);

      const newData = await Promise.all(
        sourcesResponses.map((response) => response.json())
      );

      setData(newData);
    } catch (error) {
      console.log(error);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <MainContainer>
      <ExportImportButtonsContainer className="transitioned">
        <ExportImportButton onClick={handleOpenExport}>
          экспорт БД
        </ExportImportButton>

        <ExportImportButton onClick={handleOpenImport}>
          импорт БД
        </ExportImportButton>
      </ExportImportButtonsContainer>

      <MainContent className="transitioned">
        <MainHeader>Поиск вакансий</MainHeader>
        <MainSearchContainer>
          <MainSearchInput placeholder="Профессия, должность или вакансия" />

          <MainSearchButton>
            <HiSearchCircle size={35} />
          </MainSearchButton>
        </MainSearchContainer>

        <MainLink to="/">посмотреть список</MainLink>
      </MainContent>

      <VacancyList className="transitioned">
        {vacancies.map(({ name, key }, idx) => {
          let vacanciesSalaries = 'Загружается...';
          let vacanciesQuantity = 'Поиск вакансий...';
          if (data[idx]) {
            vacanciesSalaries = `${data[idx].from}-${data[idx].to} руб.`;

            vacanciesQuantity = `${data[idx].items.length} ${plural(
              data[idx].items.length,
              ['вакансия', 'вакансии', 'вакансий']
            )}`;
          }

          return (
            <VacancyItem
              key={key}
              current={vacancyId === idx}
              onClick={() =>
                setVacancyId((prev) => {
                  setVacancyNoteShown(
                    (prevShown) => prev !== idx || !prevShown
                  );
                  return idx;
                })
              }>
              <VacancyItemHeader>{name}</VacancyItemHeader>

              {data[idx] && (
                <>
                  <VacancyItemParagraph>
                    {vacanciesSalaries}
                  </VacancyItemParagraph>
                  <VacancyItemParagraph>
                    {vacanciesQuantity}
                  </VacancyItemParagraph>
                </>
              )}
            </VacancyItem>
          );
        })}
      </VacancyList>

      <VacancyNote
        className="transitioned"
        current={vacancyNoteShown}
        vacancyId={vacancyId}>
        {vacancyNoteShown && data[vacancyId] && (
          <VacancyNoteContainer>
            {data[vacancyId].items.map(({ name, id }) => (
              <Vacancy key={id}>
                <VacancyTitle>{name}</VacancyTitle>
              </Vacancy>
            ))}
          </VacancyNoteContainer>
        )}
      </VacancyNote>

      <Modal onClose={handleExportClose} open={isExportOpen}>
        <FcDownload size={140} />
        <ModalButton>скачать файл</ModalButton>
        <ModalButton onClick={handleExportClose}>закрыть</ModalButton>
      </Modal>

      <Modal onClose={handleImportClose} open={isImportOpen}>
        <FcUpload size={140} />
        <ModalButton>загрузить файл</ModalButton>
        <ModalButton onClick={handleImportClose}>закрыть</ModalButton>
      </Modal>
    </MainContainer>
  );
}
