import {
  Button,
  Input,
  InputGroup,
  InputLeftAddon,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  Radio,
  RadioGroup,
  RangeSlider,
  RangeSliderFilledTrack,
  RangeSliderThumb,
  RangeSliderTrack,
  Select,
  Stack,
  Textarea,
  useToast,
} from '@chakra-ui/react';
import { css } from '@emotion/react';

import { useCallback, useEffect, useState } from 'react';
import { HiSearchCircle } from 'react-icons/all';

import 'beautiful-react-diagrams/styles.css';
import Diagram, { createSchema, useSchema } from 'beautiful-react-diagrams';

import { Modal, useModal, Vacancy } from '../components';
import { SERVER_URL } from '../utils/constants';
import {
  Filter,
  FilterTitle,
  FilterValues,
  ListButton,
  ListButtonLink,
  ListButtonsContainer,
  ListContent,
  ListItemsContainer,
  ListMenu,
  ListSearchButton,
  ListSearchContainer,
  ListSearchInput,
  ListStyledContainer,
} from './styles';

const initialPayload = {
  name: '',
  area_id: -1,
  currency: 'RUR',
  employer: '',
  schedule: '',
  requirement: '',
  responsibility: '',
  salary_from: 0,
  salary_to: 500000,
};

export function List({ location: { state } }) {
  const initialSearch = state?.search || '';

  const toast = useToast();

  const {
    isModalOpened: isGraphOpen,
    handleModalOpen: handleOpenGraph,
    handleModalClose: handleGraphClose,
  } = useModal();

  const {
    isModalOpened: isDiagramOpen,
    handleModalOpen: handleOpenDiagram,
    handleModalClose: handleDiagramClose,
  } = useModal();

  const {
    isModalOpened: isCreateOpen,
    handleModalOpen: handleOpenCreate,
    handleModalClose: handleCreateClose,
  } = useModal();

  const [search, setSearch] = useState(initialSearch);
  const [area, setArea] = useState(-1);
  const [salary, setSalary] = useState([0, 500000]);

  const [areaData, setAreaData] = useState([]);
  const [moreAreas, setMoreAreas] = useState(false);

  const [filteredData, setFilteredData] = useState([]);

  const [schema, { onChange }] = useSchema({});

  const [selectedVacancy, setSelectedVacancy] = useState(-1);

  const [payload, setPayload] = useState(initialPayload);

  useEffect(() => {
    fetch(`${SERVER_URL}/api/area/list?offset=0&limit=100`)
      .then((res) => res.json())
      .then((data) => {
        setAreaData(data);
      });
  }, []);

  const handleFilter = useCallback(() => {
    const payloadSearch = search || '*';
    const payloadArea = area === -1 ? '' : `&areas=${area}`;

    fetch(
      `${SERVER_URL}/api/vacancy/filter/?search_arg=${payloadSearch}${payloadArea}&currency=RUR&sf=${salary[0]}&st=${salary[1]}&offset=0&limit=100`
    )
      .then((res) => res.json())
      .then((data) => setFilteredData(data));
  }, [area, search, salary]);

  useEffect(() => {
    handleFilter();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selectedVacancy === -1) {
      return;
    }

    fetch(`${SERVER_URL}/api/vacancy/sim/${selectedVacancy}/10`)
      .then((res) => res.json())
      .then(({ cx, cy, items, name }) => {
        const newSchema = createSchema({
          nodes: [
            {
              id: selectedVacancy.toString(),
              content: name,
              coordinates: [cx, cy],
            },
            ...items.map(
              ({ cx: x, cy: y, name: content, vacancy_id: vacancyId }) => ({
                id: vacancyId.toString(),
                content,
                coordinates: [x, y],
              })
            ),
          ],
          links: items.map(({ vacancy_id: vacancyId, cnt }) => ({
            input: selectedVacancy.toString(),
            output: vacancyId.toString(),
            label: cnt,
          })),
        });

        onChange(newSchema);
      });
  }, [onChange, selectedVacancy]);

  const handleSave = useCallback(() => {
    fetch(`${SERVER_URL}/api/vacancy`, {
      method: 'post',
      body: JSON.stringify(payload),
    }).then(() => {
      setPayload(initialPayload);

      toast({
        title: 'Вакансия создана!',
        description: 'Вы успешно создали новую вакансию',
        status: 'success',
        duration: 9000,
        isClosable: true,
      });

      handleCreateClose();
    });
  }, [handleCreateClose, payload, toast]);

  const handleDelete = useCallback(
    (id) => () => {
      fetch(`${SERVER_URL}/api/vacancy/${id}`, {
        method: 'delete',
      }).then(() => {
        handleFilter();

        toast({
          title: 'Вакансия удалена',
          description: 'Вы успешно удалили вакансию',
          status: 'success',
          duration: 9000,
          isClosable: true,
        });
      });
    },
    [handleFilter, toast]
  );

  return (
    <ListStyledContainer>
      <ListMenu>
        <ListButtonLink to="/">На главную</ListButtonLink>

        <Filter>
          <FilterTitle>Регион</FilterTitle>

          <RadioGroup onChange={(value) => setArea(Number(value))} value={area}>
            <Stack>
              {areaData
                .slice(0, moreAreas ? areaData.length - 1 : 3)
                .map(({ id, name }) => (
                  <Radio
                    key={id}
                    colorScheme="green"
                    name={id}
                    size="md"
                    value={id}>
                    {name}
                  </Radio>
                ))}
            </Stack>
          </RadioGroup>
          {!moreAreas && (
            <Button
              colorScheme="blue"
              onClick={() => setMoreAreas(true)}
              variant="link">
              показать все
            </Button>
          )}
        </Filter>

        <FilterTitle>Уровень дохода</FilterTitle>
        <RangeSlider max={500000} onChange={setSalary} value={salary}>
          <RangeSliderTrack>
            <RangeSliderFilledTrack />
          </RangeSliderTrack>
          <RangeSliderThumb index={0} />
          <RangeSliderThumb index={1} />
        </RangeSlider>

        <FilterValues>
          <span>{salary[0]}</span>
          <span>{salary[1]}</span>
        </FilterValues>
      </ListMenu>
      <ListContent>
        <ListSearchContainer>
          <ListSearchInput
            onChange={({ target: { value } }) => setSearch(value)}
            onKeyDown={({ key }) => key === 'Enter' && handleFilter()}
            placeholder="Профессия, должность или вакансия"
            value={search}
          />

          <ListSearchButton onClick={handleFilter}>
            <HiSearchCircle size={35} />
          </ListSearchButton>
        </ListSearchContainer>

        <ListButtonsContainer>
          <ListButton
            onClick={() => {
              if (selectedVacancy === -1) {
                toast({
                  title: 'Выберите вакансию',
                  status: 'warning',
                  duration: 2000,
                  isClosable: true,
                });
                return;
              }

              handleOpenDiagram();
            }}>
            Построить диаграмму
          </ListButton>
          <ListButton
            onClick={() => {
              if (selectedVacancy === -1) {
                toast({
                  title: 'Выберите вакансию',
                  status: 'warning',
                  duration: 2000,
                  isClosable: true,
                });
                return;
              }

              handleOpenGraph();
            }}>
            Построить граф
          </ListButton>
          <ListButton onClick={handleOpenCreate}>
            Разместить вакансию
          </ListButton>
        </ListButtonsContainer>

        <ListItemsContainer>
          {filteredData.length > 0
            ? filteredData.map(({ id, salary_from: salaryFrom, ...rest }) => (
                <Vacancy
                  key={id}
                  {...rest}
                  onClick={() => setSelectedVacancy(id)}
                  onRemoveClick={handleDelete(id)}
                  salaryFrom={salaryFrom}
                  selected={id === selectedVacancy}
                />
              ))
            : 'Нет данных'}
        </ListItemsContainer>
      </ListContent>

      <Modal onClose={handleGraphClose} open={isGraphOpen} />

      <Modal big onClose={handleDiagramClose} open={isDiagramOpen}>
        <Diagram onChange={onChange} schema={schema} />
      </Modal>

      <Modal onClose={handleCreateClose} open={isCreateOpen}>
        <Stack
          css={css`
            width: 100%;
            height: 100%;
          `}
          spacing={3}>
          <Stack direction="row">
            <Input
              onChange={({ target: { value } }) =>
                setPayload((prev) => ({ ...prev, name: value }))
              }
              placeholder="Введите название вакансии"
              value={payload.name}
            />
            <Button colorScheme="teal" onClick={handleSave}>
              Сохранить
            </Button>
            <Button
              colorScheme="red"
              onClick={handleCreateClose}
              variant="outline">
              Отменить
            </Button>
          </Stack>

          <InputGroup>
            <InputLeftAddon>Введите заработную плату от</InputLeftAddon>
            <NumberInput
              css={css`
                width: 100%;
              `}
              onChange={(_, value) =>
                setPayload((prev) => ({ ...prev, salary_from: value }))
              }
              value={payload.salary_from}>
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </InputGroup>

          <InputGroup>
            <InputLeftAddon>Введите заработную плату до</InputLeftAddon>
            <NumberInput
              css={css`
                width: 100%;
              `}
              onChange={(_, value) =>
                setPayload((prev) => ({ ...prev, salary_to: value }))
              }
              value={payload.salary_to}>
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </InputGroup>

          <InputGroup>
            <InputLeftAddon>Введите название компании</InputLeftAddon>
            <Input
              onChange={({ target: { value } }) =>
                setPayload((prev) => ({ ...prev, employer: value }))
              }
              type="text"
              value={payload.employer}
            />
          </InputGroup>

          <Select
            onChange={({ target: { value } }) =>
              setPayload((prev) => ({ ...prev, area_id: value }))
            }
            placeholder="Выберите город"
            value={payload.area_id}>
            {areaData.map(({ id, name }) => (
              <option key={id} value={id}>
                {name}
              </option>
            ))}
          </Select>

          <Select
            onChange={({ target: { value } }) =>
              setPayload((prev) => ({ ...prev, schedule: value }))
            }
            placeholder="Выберите режим работы"
            value={payload.schedule}>
            <option value="fullDay">Полный день</option>
            <option value="remote">Удаленная работа</option>
            <option value="flexible">Гибкий график</option>
            <option value="shift">Сменный график</option>
          </Select>

          <InputGroup>
            <InputLeftAddon>Введите требования</InputLeftAddon>
            <Textarea
              onChange={({ target: { value } }) =>
                setPayload((prev) => ({ ...prev, requirement: value }))
              }
              resize="none"
              size="sm"
              value={payload.requirement}
            />
          </InputGroup>

          <InputGroup>
            <InputLeftAddon>Введите зоны ответственности</InputLeftAddon>
            <Textarea
              onChange={({ target: { value } }) =>
                setPayload((prev) => ({ ...prev, responsibility: value }))
              }
              resize="none"
              size="sm"
              value={payload.responsibility}
            />
          </InputGroup>
        </Stack>
      </Modal>
    </ListStyledContainer>
  );
}
