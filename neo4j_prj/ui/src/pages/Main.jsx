import { useToast } from '@chakra-ui/react';
import { navigate } from '@reach/router';

import { useCallback, useEffect, useState } from 'react';
import { FcDownload, FcUpload, HiSearchCircle } from 'react-icons/all';

import { saveAs } from 'file-saver';

import { Modal, useModal } from '../components';
import { SERVER_URL } from '../utils/constants';
import { plural } from '../utils/plural';
import {
  ExportImportButton,
  ExportImportButtonsContainer,
  FileInput,
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
  VacancyParagraph,
  VacancyTitle,
} from './styles';

const vacancies = [
  {
    name: 'Востребованные вакансии',
    key: 'top_need',
    url: `${SERVER_URL}/api/vacancy/top_need/0/4`,
  },
  {
    name: 'Высокооплачиваемые вакансии',
    key: 'top_paid',
    url: `${SERVER_URL}/api/vacancy/top_paid/0/4`,
  },
  {
    name: 'Новые вакансии',
    key: 'top_new',
    url: `${SERVER_URL}/api/vacancy/top_new/0/4`,
  },
];

export function Main() {
  const toast = useToast();

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

  const [search, setSearch] = useState('');

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

  const handleSearch = useCallback(() => {
    navigate('/list', { state: { search } });
  }, [search]);

  const handleExport = useCallback(() => {
    fetch(`${SERVER_URL}/api/data/export`)
      .then((res) => res.text())
      .then((base64Text) => {
        const blob = new Blob([base64Text], {
          type: 'text/plain;charset=utf-8',
        });

        saveAs(blob, 'data_export.txt');

        toast({
          title: 'База данных сохранена!',
          description: 'Вы успешно сохранили базу данных из файла',
          status: 'success',
          duration: 9000,
          isClosable: true,
        });

        handleExportClose();
      });
  }, [handleExportClose, toast]);

  const handleImport = useCallback(
    ({ target: { files } }) => {
      const [fileData] = files;

      const fileReader = new FileReader();

      fileReader.readAsText(fileData);

      fileReader.onload = () => {
        fetch(`${SERVER_URL}/api/data/import`, {
          method: 'POST',
          body: `${fileReader.result}`,
        }).then(() => {
          toast({
            title: 'База данных загружена!',
            description: 'Вы успешно загрузили базу данных из файла',
            status: 'success',
            duration: 9000,
            isClosable: true,
          });

          handleImportClose();
        });
      };
    },
    [handleImportClose, toast]
  );

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
          <MainSearchInput
            onChange={({ target: { value } }) => setSearch(value)}
            onKeyDown={({ key }) => key === 'Enter' && handleSearch()}
            placeholder="Профессия, должность или вакансия"
            value={search}
          />

          <MainSearchButton onClick={handleSearch}>
            <HiSearchCircle size={35} />
          </MainSearchButton>
        </MainSearchContainer>

        <MainLink to="/list">посмотреть список</MainLink>
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
              onClick={() => {
                if (!data[idx]) {
                  return;
                }

                setVacancyId((prev) => {
                  setVacancyNoteShown(
                    (prevShown) => prev !== idx || !prevShown
                  );
                  return idx;
                });
              }}>
              <VacancyItemHeader>{name}</VacancyItemHeader>

              <VacancyItemParagraph>{vacanciesSalaries}</VacancyItemParagraph>
              <VacancyItemParagraph>{vacanciesQuantity}</VacancyItemParagraph>
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
            {data[vacancyId].items.map(
              ({ name, id, Employer: { name: employer } }) => (
                <Vacancy key={id}>
                  <VacancyTitle>{name}</VacancyTitle>
                  <VacancyParagraph>По договоренности</VacancyParagraph>
                  <VacancyParagraph>{employer}</VacancyParagraph>
                </Vacancy>
              )
            )}
          </VacancyNoteContainer>
        )}
      </VacancyNote>

      <Modal onClose={handleExportClose} open={isExportOpen}>
        <FcDownload size={140} />
        <ModalButton onClick={handleExport}>скачать файл</ModalButton>
        <ModalButton onClick={handleExportClose}>закрыть</ModalButton>
      </Modal>

      <Modal onClose={handleImportClose} open={isImportOpen}>
        <FcUpload size={140} />
        <FileInput>
          загрузить файл
          <input
            accept=".txt"
            onChange={handleImport}
            placeholder="загрузить файл"
            type="file"
          />
        </FileInput>
        <ModalButton onClick={handleImportClose}>закрыть</ModalButton>
      </Modal>
    </MainContainer>
  );
}
